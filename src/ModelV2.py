import itertools
import json
import pandas as pd
import pycountry_convert as pc

class Model:
    def __init__(self) -> None:
        self._df: pd.DataFrame = pd.DataFrame()
        pass

    def load_data(self, file: str):
        records = []
        with open(file) as f:
            for line in f:
                records.append(json.loads(line))
        self._df = pd.DataFrame.from_records(records)

    def view_by_country(self, doc_id: str, print=False):
        """
        Return the dataframe
        The values are in the column "visitor_country"
        """
        docs_views_country = self._df.loc[(self._df["subject_doc_id"] == doc_id) & (self._df["event_type"] == "impression")]
        if print == True:
            print(docs_views_country)
        return docs_views_country

    def view_by_continent(self, doc_id: str, print=False):
        """
        Return the dataframe
        The values are in the column "continent"
        """
        docs_views_continent = self.view_by_country(doc_id=doc_id)
        def normalize(val: str):
            return pc.country_alpha2_to_continent_code(val)
        docs_views_continent["continent"] = docs_views_continent["visitor_country"].apply(normalize)
        if print == True:
            print(docs_views_continent)
        return docs_views_continent

    def view_by_browser(self, print=False):
        """
        Return the dataframe
        The values are in the column "browser" (normalized from the "visitor_useragent" column)
        """
        docs_views_browser = self._df
        def normalize(val: str):
            return "".join(val.split("/")[:1])
        docs_views_browser["browser"] = docs_views_browser["visitor_useragent"].apply(normalize)
        if print == True:
            print(docs_views_browser)
        return docs_views_browser

    def reader_profile(self, print=False):
        """
        Return the dataframe
        `x.head(10)` to show the 10 most readers
        """
        docs_reader_profile = self._df.loc[(self._df["event_type"] == "pagereadtime")]
        docs_reader_profile = docs_reader_profile.groupby(["visitor_uuid"])[["event_readtime"]].sum()
        docs_reader_profile = docs_reader_profile.sort_values(by=["event_readtime"], ascending=False)
        if print == True:
            print(docs_reader_profile)
        return docs_reader_profile

    def _viewers_for(self, doc_id: str):
        """
        Return the list of viewer for a document
        """
        viewers = self._df.loc[(self._df["subject_doc_id"] == doc_id) & (self._df["event_type"] == "impression")]
        return viewers["visitor_uuid"].unique()

    def _document_read_for(self, user_id: str):
        """
        Return the list of document read by a user
        """
        document = self._df.loc[(self._df["visitor_uuid"] == user_id) & (self._df["event_type"] == "impression")]
        return document["subject_doc_id"].unique()

    def also_likes(self, doc_id: str, user_id: str, sort):
        """
        Return list of documents the user can likes based on others reader and what they read.
        The sorting function take a list[tuple[doc_id, number_of_occurence]]
        The result is the result of the sort function
        """
        viewers_for_doc = self._viewers_for(doc_id)
        doc_already_read = self._document_read_for(user_id)
        all_documents = []
        for doc_viewer in viewers_for_doc:
            docs_read = self._document_read_for(doc_viewer)
            all_documents.extend(docs_read)
        res_iter = itertools.groupby(all_documents)
        res = [
            (key, len(list(group)))
            for key, group in res_iter
            if key not in doc_already_read
        ]
        res = sort(res)
        return res

    @staticmethod
    def sort_default(docs):
        """
        Return a list of document sorted by the number of occurence
        The return is list[str]
        """
        sorted_by_cross_view = sorted(
            docs,
            key=lambda y: y[1],
            reverse=True
        )
        return [
            z[0]
            for z in sorted_by_cross_view
        ]

    def also_likes_default(self, doc_id: str, user_id: str):
        """
        Same as ModelV2.also_likes with the ModelV2.sort_default as sort function
        """
        return self.also_likes(doc_id, user_id, self.sort_default)
    
    def _event_type_unique(self):
        """
        Return a list of "event_type"
        """
        return self._df["event_type"].unique()