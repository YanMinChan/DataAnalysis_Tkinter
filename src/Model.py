import itertools
import json
from typing import Any, Callable, TypeVar
import pandas as pd
import pycountry_convert as pc

SortType = TypeVar("SortType")


class Model:
    def __init__(self) -> None:
        self._df: pd.DataFrame = pd.DataFrame()
        pass

    def load_data(self, file: str | Any):
        records: list[Any] = []
        if isinstance(file, str):
            with open(file) as f:
                for line in f:
                    records.append(json.loads(line))
        else:
            for line in file:
                records.append(json.loads(line))
        self._df = pd.DataFrame.from_records(records)

    def view_by_country(self, doc_id: str, debug: bool = False) -> pd.DataFrame:
        """
        Return the dataframe
        The values are in the column "visitor_country"
        """
        docs_views_country = self._df.loc[
            (self._df["subject_doc_id"] == doc_id)
            & (self._df["event_type"] == "impression")
        ]
        if debug == True:
            print(docs_views_country)
        return docs_views_country

    def view_by_continent(self, doc_id: str, debug: bool = False) -> pd.DataFrame:
        """
        Return the dataframe
        The values are in the column "continent"
        """
        docs_views_continent = self.view_by_country(doc_id=doc_id)

        def normalize(val: str) -> str:
            return pc.country_alpha2_to_continent_code(val)

        docs_views_continent = docs_views_continent.assign(
            continent=docs_views_continent["visitor_country"]
        )
        docs_views_continent["continent"] = docs_views_continent["continent"].apply(
            normalize
        )
        if debug == True:
            print(docs_views_continent)
        return docs_views_continent

    def view_by_browser(self, debug: bool = False) -> pd.DataFrame:
        """
        Return the dataframe
        The values are in the column "browser" (normalized from the "visitor_useragent" column)
        """
        docs_views_browser = self._df

        def normalize(val: Any):
            if isinstance(val, str):
                return "".join(val.split("/")[:1])
            return ""

        docs_views_browser = docs_views_browser.assign(
            browser=docs_views_browser["visitor_useragent"]
        )
        docs_views_browser["browser"] = docs_views_browser["browser"].apply(normalize)
        if debug == True:
            print(docs_views_browser)
        return docs_views_browser

    def reader_profile(self, debug: bool = False) -> pd.DataFrame:
        """
        Return the dataframe
        `x.head(10)` to show the 10 most readers
        """
        docs_reader_profile = self._df.loc[(self._df["event_type"] == "pagereadtime")]
        docs_reader_profile = docs_reader_profile.groupby(["visitor_uuid"])[
            ["event_readtime"]
        ].sum()
        docs_reader_profile = docs_reader_profile.sort_values(
            by=["event_readtime"], ascending=False
        )
        if debug == True:
            print(docs_reader_profile)
        return docs_reader_profile

    def _viewers_for(self, doc_id: str) -> set[str]:
        """
        Return the list of viewer for a document
        """
        viewers = self._df.loc[
            (self._df["subject_doc_id"] == doc_id)
            & (self._df["event_type"] == "impression")
        ]
        return set(viewers["visitor_uuid"].unique())

    def _document_read_for(self, user_id: str) -> set[str]:
        """
        Return the list of document read by a user
        """
        document = self._df.loc[
            (self._df["visitor_uuid"] == user_id)
            & (self._df["event_type"] == "impression")
        ]
        return set(document["subject_doc_id"].unique())

    def also_likes(
        self,
        doc_id: str,
        user_id: str,
        sort: Callable[[list[tuple[str, int]]], SortType],
    ) -> SortType:
        """
        Return list of documents the user can likes based on others reader and what they read.
        The sorting function take a list[tuple[doc_id, number_of_occurence]]
        The result is the result of the sort function
        """
        viewers_for_doc = self._viewers_for(doc_id)
        doc_already_read = self._document_read_for(user_id)
        all_documents: list[str] = []
        for doc_viewer in viewers_for_doc:
            docs_read = self._document_read_for(doc_viewer)
            all_documents.extend(docs_read)
        res_iter = itertools.groupby(all_documents)
        res: list[tuple[str, int]] = [
            (key, len(list(group)))
            for key, group in res_iter
            if key not in doc_already_read
        ]
        res_sort = sort(res)
        return res_sort

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
