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

    def reader_profile_text(self) -> str:
        profiles = self._model.reader_profile()
        s = repr(profiles)
        return s


if __name__ == "__main__":
    import os

    cnt = Controller(Model())
    cnt.load_file(os.path.join(os.path.dirname(__file__), "..", "sample_small.json"))
    cnt.reader_profile_graph()
    cnt.reader_profile_text()
    _ = input()
