import numpy as np
import matplotlib.pyplot as plt
import GraphViz
from Model import Model


class Controller:
    def __init__(self, model: Model) -> None:
        self._model: Model = model

    def load_file(self, file: str, disable_cache: bool = False):
        self._model.load_data(file, disable_cache)

    def reader_profile_graph(self) -> None:
        """
        Return a horizontal bar plot of the top 10 reader and their total time spent
        """
        profiles = self._model.reader_profile()

        values = [float(y[0]) for y in profiles[["event_readtime"]].head(10).values]
        labels = ["*" + label[-4:] for label in profiles.head(10).index]
        fig, ax = plt.subplots()
        ax.barh(width=values, y=labels, linewidth=0.7)
        ax.set_ylabel("Reader user ID (last four characters)")
        ax.set_xlabel("Total time spent (seconds)")
        ax.set_title("Reader profile")
        fig.show()

    # Return the top 10 reader
    def reader_profile_text(self) -> str:
        """
        Return the top 10 reader and their total time spent in text
        """
        profiles = self._model.reader_profile()
        s = profiles.head(10).to_string()
        return s

    def view_by_full_browser_text(self, event_type: str) -> str:
        """
        Return the number of occurrences of each main browser in text
        """
        df = self._model.view_by_browser(event_type=event_type)
        s = df["visitor_useragent"].value_counts().to_string()
        return s

    def view_by_full_browser_graph(self, event_type: str) -> None:
        """
        Return a bar plot of the number of occurrences of each main browsers
        """
        browsers = self._model.view_by_browser(event_type=event_type)[
            "visitor_useragent"
        ]
        values = [float(y) for y in browsers.value_counts().values]
        labels = [
            label[:20] for label in browsers.value_counts().index
        ]  # cut short the label length to 20 char
        fig, ax = plt.subplots()
        ax.bar(height=values, x=labels)
        ax.set_xlabel("Browser")
        ax.tick_params("x", labelsize=8, rotation=90)  # avoid label overcrowding
        ax.set_ylabel("Total number of occurrences")
        ax.set_title('Views by browser (event_type="' + event_type + '")')
        fig.show()

    def view_by_browser_text(self, event_type: str) -> str:
        """
        Return the number of occurrences of each main browser in text
        """
        df = self._model.view_by_browser(event_type=event_type)
        s = df["browser"].value_counts().to_string()
        return s

    def view_by_browser_graph(self, event_type: str) -> None:
        """
        Return a bar plot of the number of occurrences of each main browsers
        """
        browsers = self._model.view_by_browser(event_type=event_type)["browser"]
        values = [float(y) for y in browsers.value_counts().values]
        labels = [label[:20] for label in browsers.value_counts().index]
        fig, ax = plt.subplots()
        ax.bar(height=values, x=labels)
        ax.set_xlabel("Main browser")
        ax.tick_params("x", labelsize=8, rotation=90)
        ax.set_ylabel("Total number of occurrences")
        ax.set_title('Views by main browser (event_type="' + event_type + '")')
        fig.show()

    def also_like_text(self, docID: str, userID: str, top: int = 10) -> str:
        likes, _ = self._model.also_likes(
            doc_id=docID, user_id=userID, sort=Model.sort_show_weight
        )
        text = ""
        for item in likes[:top]:
            text += f"- {item[0]} : {item[1]}\n"
        return text

    def also_like_graph(self, docID: str, userID: str, top: int = 10):
        _, graph = self._model.also_likes(
            doc_id=docID, user_id=userID, sort=Model.sort_show_weight
        )
        GraphViz.render(user_id=userID, doc_id=docID, graph=graph)

    def view_by_country_graph(self, docID: str):
        countries = self._model.view_by_country(doc_id=docID)["visitor_country"]
        values = [float(y) for y in countries.value_counts().values]
        labels = [label for label in countries.value_counts().index]
        fig, ax = plt.subplots()
        ax.bar(height=values, x=labels)
        ax.set_xlabel("Country")
        ax.set_ylabel("Total number of occurrences")
        ax.set_title("Views by country of document " + "*" + docID[-4:])
        fig.show()

    def view_by_country_text(self, docID: str):
        countries = self._model.view_by_country(doc_id=docID)["visitor_country"]
        return countries.value_counts().to_string()

    def view_by_continent_graph(self, docID: str):
        continents = self._model.view_by_continent(doc_id=docID)["continent"]
        values = [float(y) for y in continents.value_counts().values]
        labels = [label for label in continents.value_counts().index]
        fig, ax = plt.subplots()
        ax.bar(height=values, x=labels)
        ax.set_xlabel("Continent")
        ax.set_ylabel("Total number of occurrences")
        ax.set_title("Views by continent of document " + "*" + docID[-4:])
        fig.show()

    def view_by_continent_text(self, docID: str):
        continents = self._model.view_by_continent(doc_id=docID)["continent"]
        return continents.value_counts().to_string()


if __name__ == "__main__":
    import os

    cnt = Controller(Model())
    cnt.load_file(
        os.path.join(os.path.dirname(__file__), "..", "samples", "sample_small.json")
    )
    cnt.reader_profile_graph()
    res = cnt.reader_profile_text()
    print(res)
    _ = input()
