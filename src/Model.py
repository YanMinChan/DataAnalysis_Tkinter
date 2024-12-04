import itertools
import orjson
import mmap
import os
from typing import Any, Callable, Generator, TypeVar
import pandas as pd
import pycountry_convert as pc
from time import perf_counter


SortType = TypeVar("SortType")

def _read_generator(mmap_file: mmap.mmap) -> Generator[bytes, Any, Any]:
    while mmap_file.tell() != mmap_file.size():
        line = mmap_file.readline()
        if len(line) == 0:
            continue
        yield line


class Model:
    def __init__(self) -> None:
        self._df: pd.DataFrame = pd.DataFrame()
        pass

    def load_data(self, file: str | Any, debug: bool = True):
        start = perf_counter()

        records: list[Any] = []
        provided_file_obj = not isinstance(file, str)
        if not provided_file_obj:
            file = open(file, mode="r", encoding='utf-8')
        # map file to RAM for faster read time
        with mmap.mmap(file.fileno(), length=0, access=mmap.ACCESS_READ) as f:
            for line in _read_generator(f):
                records.append(orjson.loads(line))
        if not provided_file_obj:
            file.close()
        between = perf_counter()
        self._df = pd.DataFrame.from_records(records)

        end = perf_counter()
        if debug:
            print("load_data:json", between - start, "seconds")
            print("load_data:pd", end - between, "seconds")

    def view_by_country(self, doc_id: str, debug: bool = False) -> pd.DataFrame:
        """
        Return the dataframe
        The values are in the column "visitor_country"
        """
        start = perf_counter()

        docs_views_country = self._df.loc[
            (self._df["env_doc_id"] == doc_id)
            & (self._df["event_type"] == "impression")
        ]

        end = perf_counter()
        if debug == True:
            print("view_by_country", end - start, "seconds")

        return docs_views_country

    def view_by_continent(self, doc_id: str, debug: bool = False) -> pd.DataFrame:
        """
        Return the dataframe
        The values are in the column "continent"
        """
        start = perf_counter()

        docs_views_continent = self.view_by_country(doc_id=doc_id)

        def normalize(val: str) -> str:
            return pc.country_alpha2_to_continent_code(val)

        docs_views_continent = docs_views_continent.assign(
            continent=docs_views_continent["visitor_country"]
        )
        docs_views_continent["continent"] = docs_views_continent["continent"].apply(
            normalize
        )

        end = perf_counter()
        if debug == True:
            print("view_by_continent", end - start, "seconds")
        return docs_views_continent

    def view_by_browser(self, debug: bool = False) -> pd.DataFrame:
        """
        Return the dataframe
        The values are in the column "browser" (normalized from the "visitor_useragent" column)
        """
        start = perf_counter()

        docs_views_browser = self._df

        def normalize(val: Any):
            if isinstance(val, str):
                return "".join(val.split("/")[:1])
            return ""

        docs_views_browser = docs_views_browser.assign(
            browser=docs_views_browser["visitor_useragent"]
        )
        docs_views_browser["browser"] = docs_views_browser["browser"].apply(normalize)

        end = perf_counter()
        if debug == True:
            print("view_by_browser", end - start, "seconds")
        return docs_views_browser

    def reader_profile(self, top: int = 10, debug: bool = True) -> pd.DataFrame:
        """
        Return the dataframe
        """
        start = perf_counter()

        docs_reader_profile = self._df.loc[(self._df["event_type"] == "pagereadtime")]
        docs_reader_profile = docs_reader_profile.groupby(["visitor_uuid"])[
            ["event_readtime"]
        ].sum().head(top)
        docs_reader_profile = docs_reader_profile.sort_values(
            by=["event_readtime"], ascending=False
        )

        end = perf_counter()
        if debug == True:
            print("reader_profile", end - start, "seconds")
        return docs_reader_profile

    def _viewers_for(self, doc_id: str) -> set[str]:
        """
        Return the list of viewer for a document
        """
        viewers = self._df.loc[
            (self._df["env_doc_id"] == doc_id)
            & (self._df["event_type"] == "impression")
        ]
        return set(viewers["visitor_uuid"].unique())

    def _document_read_for(self, user_id: str | list[str]) -> pd.DataFrame:
        """
        Return the list of document read by a user
        """
        mask = None
        if isinstance(user_id, str):
            mask = self._df["visitor_uuid"] == user_id
        else:
            mask = self._df["visitor_uuid"].isin(user_id)
        document = self._df.loc[
            (mask)
            & (self._df["event_type"] == "impression")
        ]
        document = document.drop_duplicates(subset=["env_doc_id", "visitor_uuid"])
        return document

    def also_likes(
        self,
        doc_id: str,
        user_id: str,
        sort: Callable[[list[tuple[str, int]]], SortType],
        with_graph: bool = False,
        debug: bool = True,
    ) -> tuple[SortType, pd.DataFrame]:
        """
        Return list of documents the user can likes based on others reader and what they read.
        The sorting function take a list[tuple[doc_id, number_of_occurence]]
        The result is the result of the sort function
        """
        start = perf_counter()

        viewers_for_doc = self._viewers_for(doc_id)
        doc_already_read = self._document_read_for(user_id)["env_doc_id"].unique()
        all_documents = self._document_read_for(list(viewers_for_doc))
        reco = all_documents.value_counts(subset=["env_doc_id"])
        print(reco)
        res_iter = [(key[0], int(reco[key[0]])) for key in reco.index if key[0] not in doc_already_read]
        res_sort = sort(res_iter)

        end = perf_counter()
        if debug:
            print("also_likes", end - start, "seconds")
        return res_sort, all_documents

    @staticmethod
    def sort_default(docs: list[tuple[str, int]]) -> list[str]:
        """
        Return a list of document sorted by the number of occurence
        The return is list[str]
        """
        sorted_by_cross_view = Model.sort_show_weight(docs)
        return [z[0] for z in sorted_by_cross_view]

    @staticmethod
    def sort_show_weight(docs: list[tuple[str, int]]) -> list[tuple[str, int]]:
        sorted_by_cross_view = sorted(docs, key=lambda y: y[1], reverse=True)
        return sorted_by_cross_view

    def also_likes_default(self, doc_id: str, user_id: str):
        """
        Same as ModelV2.also_likes with the ModelV2.sort_default as sort function
        """
        return self.also_likes(doc_id, user_id, Model.sort_default)

    def event_type_unique(self) -> set[str]:
        """
        Return a list of "event_type"
        """
        return set(self._df["event_type"].unique())


if __name__ == "__main__":
    import os
    import GraphViz

    model = Model()
    model.load_data(os.path.join(os.path.dirname(__file__), "..", "sample_small.json"))
    doc_id = "120111003737-ff0d62c2f9e64064b73f058095e4f081"
    user_id = "b417fd6f88d6516d"
    df = model.view_by_country(doc_id)
    print(df["visitor_country"].unique())

    df = model.view_by_continent(doc_id)
    print(df["continent"].unique())

    df = model.view_by_browser()
    print(df["browser"].value_counts())

    df = model.reader_profile()
    print(df.head(10))

    df = model.also_likes_default(doc_id=doc_id, user_id=user_id)
    print(df)

    # more tests
    model = Model()
    model.load_data(os.path.join(os.path.dirname(__file__), "..", "sample_3m_lines.json"))
    document = model._df.loc[
        (model._df["event_type"] == "impression")
    ]["env_doc_id"].value_counts()
    print(document)

    sorts, graph = model.also_likes_default("121109150636-bdf13c63b3964e1494a82f6c144024e2", "d9c9f5e099ac4746")
    print(graph)
    GraphViz.render("d9c9f5e099ac4746", "121109150636-bdf13c63b3964e1494a82f6c144024e2", sorts, graph)
    print(df)
