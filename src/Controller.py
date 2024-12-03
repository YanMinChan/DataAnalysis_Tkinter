import numpy as np
import matplotlib.pyplot as plt
from Model import Model


class Controller:
    def __init__(self, model: Model) -> None:
        self._model: Model = model

    def load_file(self, file: str):
        self._model.load_data(file)

    def reader_profile_graph(self) -> None:
        """
        Return a horizontal bar plot of the top 10 reader and their total time spent
        """
        profiles = self._model.reader_profile()

        values = [float(y[0]) for y in profiles[["event_readtime"]].head(10).values]
        labels = ["*" + label[-4:] for label in profiles.head(10).index]
        plt.barh(width=values, y=labels, linewidth=0.7)
        plt.ylabel("Reader user ID (last four characters)")
        plt.xlabel("Total time spent")
        plt.title("Reader profile")
        plt.show()

    # Return the top 10 reader
    def reader_profile_text(self) -> str:
        """
        Return the top 10 reader and their total time spent in text
        """
        profiles = self._model.reader_profile()
        s = repr(profiles.head(10))
        return s

    def view_by_browser_text(self, event_type: str) -> str:
        """
        Return the number of occurrences of each main browser in text
        """
        df = self._model.view_by_browser()
        s = repr(df["browser"].value_counts())
        return s

    def view_by_browser_graph(self, event_type: str) -> None:
        """
        Return a bar plot of the number of occurrences of each main browsers
        """
        # occurrence for different "event_type" not implemented yet
        browsers = self._model.view_by_browser()["browser"]
        values = [float(y) for y in browsers.value_counts().values]
        labels = [label for label in browsers.value_counts().index]
        plt.bar(height=values, x=labels)
        plt.xlabel("Main browser")
        plt.ylabel("Total number of occurrences")
        plt.title("Views by browser")
        plt.show()

    def also_like_text(self, docID: str, userID: str) -> str:
        likes = self._model.also_likes(
            doc_id=docID, user_id=userID, sort=Model.sort_show_weight
        )
        text = ""
        for item in likes:
            text += f"- {item[0]} : {item[1]}\n"
        return text

    def also_like_graph(self, docID: str, userID: str) -> str:
        pass

    def view_by_country_graph(self, docID: str):
        countries = self._model.view_by_country(doc_id=docID)["visitor_country"]
        values = [float(y) for y in countries.value_counts().values]
        labels = [label for label in countries.value_counts().index]
        plt.bar(height=values, x=labels)
        plt.xlabel("Country")
        plt.ylabel("Total number of occurrences")
        plt.title("Views by country of document " + "*" + docID[-4:])
        plt.show()

    def view_by_continent_graph(self, docID: str):
        continents = self._model.view_by_continent(doc_id=docID)["continent"]
        values = [float(y) for y in continents.value_counts().values]
        labels = [label for label in continents.value_counts().index]
        plt.bar(height=values, x=labels)
        plt.xlabel("Continent")
        plt.ylabel("Total number of occurrences")
        plt.title("Views by continent of document " + "*" + docID[-4:])
        plt.show()


if __name__ == "__main__":
    import os

    cnt = Controller(Model())
    cnt.load_file(os.path.join(os.path.dirname(__file__), "..", "sample_small.json"))
    cnt.reader_profile_graph()
    cnt.reader_profile_text()
    _ = input()
