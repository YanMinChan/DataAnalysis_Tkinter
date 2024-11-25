import tkinter as tk
from typing import override
from Controller import Controller
from Model import Model


class Window(tk.Tk):
    def __init__(
        self,
        controller: Controller,
        *args,  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
        **kwargs,  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
    ):
        self.cnt: Controller = controller
        super().__init__(*args, **kwargs)  # pyright: ignore[reportUnknownArgumentType]
        self.title("Home")
        self.geometry("340x200")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        _ = container.grid_rowconfigure(0, weight=1)
        _ = container.grid_columnconfigure(0, weight=1)

        self.frames: dict[type, PopUp] = {}
        menu = tk.Menu(self)
        menu_i = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Features", menu=menu_i)

        for f in (
            BlankPage,
            ViewByCountryPage,
            ViewByContinentPage,
            ViewByBrowser,
            ViewByMainBrowser,
            ReaderProfiles,
            AlsoLikes,
        ):
            self.frames[f] = f(container, self)
            self.frames[f].grid(row=0, column=0, stick="nsew")
            menu_i.add_command(
                label=self.frames[f].page_name, command=self.frames[f].go_to
            )

        self.select_frame(BlankPage)
        _ = self.config(menu=menu)

    def select_frame(self, frame: type):
        self.frames[frame].tkraise()


class PopUp(tk.Frame):
    page_name: str

    def __init__(self, parent: tk.Frame, window: Window, page_name: str):
        self.window: Window = window
        self.page_name = page_name
        super().__init__(parent)

    def go_to(self):
        self.window.select_frame(type(self))
        self.window.title(self.page_name)


# The Home page (blank)
class BlankPage(PopUp):
    def __init__(self, parent: tk.Frame, window: Window):
        super().__init__(parent, window, "Home")

    @override
    def go_to(self):
        super().go_to()


# The view by country page
class ViewByCountryPage(PopUp):
    def __init__(self, parent: tk.Frame, window: Window):
        super().__init__(parent, window, "View by Country")

        _ = self.columnconfigure(0, weight=1)
        _ = self.columnconfigure(1, weight=4)

        # The input boxes
        label = tk.Label(self, text="Document UUID")
        label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.docID: tk.StringVar = tk.StringVar()  # store docID value
        docID_entry = tk.Entry(self, textvariable=self.docID)
        docID_entry.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=5)

        # The buttons
        view_by_country_button = tk.Button(
            self, text="Ok", command="view_by_country_clicked"
        )
        view_by_country_button.grid(row=1, column=1, ipadx=10, pady=5)

    @override
    def go_to(self):
        super().go_to()


# The view by continent page
class ViewByContinentPage(PopUp):
    def __init__(self, parent: tk.Frame, window: Window):
        super().__init__(parent, window, "View by Continent")

        _ = self.columnconfigure(0, weight=1)
        _ = self.columnconfigure(1, weight=4)

        # The input boxes
        label = tk.Label(self, text="Document UUID")
        label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.docID: tk.StringVar = tk.StringVar()  # store docID value
        docID_entry = tk.Entry(self, textvariable=self.docID)
        docID_entry.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=5)

        # The buttons
        view_by_continent_button = tk.Button(
            self, text="Ok", command="view_by_continent_clicked"
        )
        view_by_continent_button.grid(row=1, column=1, ipadx=10, pady=5)

    @override
    def go_to(self):
        super().go_to()


class ViewByBrowser(PopUp):

    def __init__(self, parent: tk.Frame, window: Window):
        super().__init__(parent, window, "View by Browser")

        _ = self.columnconfigure(0, weight=1)
        _ = self.columnconfigure(1, weight=4)

        # The menu of event type
        label = tk.Label(self, text="Event type")
        label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        event_name = tk.StringVar()
        options = [
            "a",
            "b",
            "c",
        ]  # CHANGE THIS ONEEEEEEEE TO A METHOD THAT RECEIVE EVENT TYPE FROM MODEL.PY!!!!!!!!!!!!!
        event_optionMenu = tk.OptionMenu(self, event_name, *options)
        event_optionMenu.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=5)

        # The buttons
        view_by_browser_button = tk.Button(
            self, text="Ok", command="view_by_browser_clicked"
        )
        view_by_browser_button.grid(row=1, column=1, ipadx=10, pady=5)

    @override
    def go_to(self):
        super().go_to()


class ViewByMainBrowser(PopUp):

    def __init__(self, parent: tk.Frame, window: Window):
        super().__init__(parent, window, "View by Main Browser")

        _ = self.columnconfigure(0, weight=1)
        _ = self.columnconfigure(1, weight=4)

        # The menu of event type
        label = tk.Label(self, text="Event type")
        label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        event_name = tk.StringVar()
        options = [
            "a",
            "b",
            "c",
        ]  # CHANGE THIS ONEEEEEEEE TO A METHOD THAT RECEIVE EVENT TYPE FROM MODEL.PY!!!!!!!!!!!!!
        event_optionMenu = tk.OptionMenu(self, event_name, *options)
        event_optionMenu.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=5)

        # The buttons
        view_by_main_browser_button = tk.Button(
            self, text="Ok", command="view_by_main_browser_clicked"
        )
        view_by_main_browser_button.grid(row=1, column=1, ipadx=10, pady=5)

    @override
    def go_to(self):
        super().go_to()


class ReaderProfiles(PopUp):
    def __init__(self, parent: tk.Frame, window: Window):
        super().__init__(parent, window, "Reader Profiles")

        # GUI column design
        _ = self.columnconfigure(0, weight=1)
        _ = self.columnconfigure(1, weight=4)

        self.text: tk.Text = tk.Text(self)
        self.text.insert(tk.INSERT, "")
        self.text.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)

        btn_text = tk.Button(self, text="Ok", command=self.on_btn_text_clicked)
        btn_text.grid(row=1, column=1, ipadx=10, pady=5)

        btn_graph = tk.Button(
            self, text="Generate graph", command=self.on_btn_graph_clicked
        )
        btn_graph.grid(row=2, column=1, ipadx=10, pady=5)

    def on_btn_text_clicked(self):
        s = self.window.cnt.reader_profile_text()
        self.text.insert(tk.END, s)
        self.text.update()

    def on_btn_graph_clicked(self):
        self.window.cnt.reader_profile_graph()

    @override
    def go_to(self):
        super().go_to()


class AlsoLikes(PopUp):
    def __init__(self, parent: tk.Frame, window: Window):
        super().__init__(parent, window, "Also Likes")

        # GUI column design
        _ = self.columnconfigure(0, weight=1)
        _ = self.columnconfigure(1, weight=4)

        # The input boxes
        label = tk.Label(self, text="Document UUID")
        label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.docID: tk.StringVar = tk.StringVar()  # store docID value
        docID_entry = tk.Entry(self, textvariable=self.docID)
        docID_entry.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=5)

        # The buttons
        also_likes_button = tk.Button(self, text="Ok", command="also_likes_clicked")
        also_likes_button.grid(row=1, column=1, ipadx=10, pady=5)
        also_likes_generate_graph = tk.Button(
            self, text="Generate graph", command="also_likes_generate_graph_clicked"
        )
        also_likes_generate_graph.grid(row=2, column=1, ipadx=10, pady=5)

    @override
    def go_to(self):
        super().go_to()


if __name__ == "__main__":
    import os

    mdl = Model()
    cnt = Controller(mdl)
    cnt.load_file(os.path.join(os.path.dirname(__file__), "..", "sample_small.json"))
    win = Window(cnt)
    win.mainloop()
