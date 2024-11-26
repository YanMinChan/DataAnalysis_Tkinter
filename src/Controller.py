import numpy as np
import matplotlib.pyplot as plt
from Model import Model


class Controller:
    def __init__(self, model: Model) -> None:
        self._model: Model = model

    def load_file(self, file: str):
        self._model.load_data(file)

    def reader_profile_graph(self) -> None:
        profiles = self._model.reader_profile()
        fig, ax = plt.subplots()
        positions = np.arange(10)
        values = [float(y[0]) for y in profiles[["event_readtime"]].head(10).values]
        labels = [label for label in profiles.head(10).index]
        bar_container = ax.barh(
            width=values, y=positions, height=1, linewidth=0.7, align="edge"
        )
        _ = ax.bar_label(bar_container, labels=labels)
        fig.show()

    def view_by_browser_text(self, event_type: str) -> str:
        df = self._model.view_by_browser()
        s = repr(df["browser"].value_counts())
        return s
    
    def view_by_browser_graph(self) -> None:
        df = self._model.view_by_browser()
        browsers = df["browser"].unique()
        fig, ax = plt.subplots()
        positions = np.arange(len(browsers))
        values = [float(y) for y in df["browser"].value_counts().values]
        labels = [label for label in df["browser"].value_counts().index]
        bar_container = ax.bar(
            height=values, x=positions, width=1, align="edge"
        )
        _ = ax.bar_label(bar_container, labels=labels)
        fig.show()

    def reader_profile_text(self) -> str:
        profiles = self._model.reader_profile()
        s = repr(profiles.head(10))
        return s
    
    def also_like_text(self, docID: str, userID: str) -> str:
        likes = self._model.also_likes(doc_id=docID, user_id=userID, sort=Model.sort_show_weight)
        text = ""
        for item in likes:
            text += f"- {item[0]} : {item[1]}\n"
        return text


if __name__ == "__main__":
    import os

    cnt = Controller(Model())
    cnt.load_file(os.path.join(os.path.dirname(__file__), "..", "sample_small.json"))
    cnt.reader_profile_graph()
    cnt.reader_profile_text()
    _ = input()
