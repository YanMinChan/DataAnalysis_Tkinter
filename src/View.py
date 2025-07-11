import sys
import tkinter as tk
from tkinter.messagebox import showerror, showinfo
import tkinter.ttk as ttk
from tkinter.filedialog import askopenfilename
from typing import override
from Controller import Controller
from GraphViz import GraphvizError
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
        self.title("Also Likes")
        self.geometry("340x200")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        _ = container.grid_rowconfigure(0, weight=1)
        _ = container.grid_columnconfigure(0, weight=1)

        self.frames: dict[type, PopUp] = {}
        menu = tk.Menu(self)
        menu_i = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Features", menu=menu_i)
        menu.add_command(label="Load File", command=self.on_btn_load_file)

        for f in (
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

        self.select_frame(AlsoLikes)
        _ = self.config(menu=menu)

    def select_frame(self, frame: type):
        self.frames[frame].tkraise()

    def on_btn_load_file(self):
        file = askopenfilename(defaultextension=".json")
        if isinstance(file, str):  # pyright: ignore[reportUnnecessaryIsInstance]
            self.cnt.load_file(file)
            _ = showinfo("File Loaded", f"The file {file} was loaded sucessfully")


class PopUp(tk.Frame):
    page_name: str

    def __init__(self, parent: tk.Frame, window: Window, page_name: str):
        self.window: Window = window
        self.page_name = page_name
        super().__init__(parent)

    def go_to(self):
        self.window.select_frame(type(self))
        self.window.title(self.page_name)


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
            self, text="Ok", command=self.view_by_country_clicked
        )
        view_by_country_button.grid(row=1, column=1, ipadx=10, pady=5)

    def view_by_country_clicked(self):
        try:
            self.window.cnt.view_by_country_graph(docID=self.docID.get())
        except ValueError as error:
            print(f"F21SCCW2: error: {error}", file=sys.stderr)
            _ = showerror("Model error", str(error))

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
            self, text="Ok", command=self.view_by_continent_clicked
        )
        view_by_continent_button.grid(row=1, column=1, ipadx=10, pady=5)

    def view_by_continent_clicked(self):
        try:
            self.window.cnt.view_by_continent_graph(docID=self.docID.get())
        except ValueError as error:
            print(f"F21SCCW2: error: {error}", file=sys.stderr)
            _ = showerror("Model error", str(error))

    @override
    def go_to(self):
        super().go_to()


class ViewByBrowser(PopUp):

    def __init__(self, parent: tk.Frame, window: Window):
        super().__init__(parent, window, "View by Browser")

        _ = self.columnconfigure(0, weight=1)
        _ = self.columnconfigure(1, weight=4)

        self.inited: bool = False

        # The menu of event type
        label = tk.Label(self, text="Event type")
        label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.event_name = tk.StringVar()

        # The buttons
        view_by_browser_button = tk.Button(
            self, text="Ok", command=self.view_by_browser_clicked
        )
        view_by_browser_button.grid(row=1, column=1, ipadx=10, pady=5)

    def init(self):
        if not self.inited:
            try:
                options = (
                    self.window.cnt._model.event_type_unique()
                )
            except ValueError as error:
                print(f"F21SCCW2: error: {error}", file=sys.stderr)
                _ = showerror("Model error", str(error))
            else:
                event_optionMenu = tk.OptionMenu(self, self.event_name, *options)
                event_optionMenu.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=5)
                self.inited = True

    def view_by_browser_clicked(self):
        self.init()
        try:
            self.window.cnt.view_by_full_browser_graph(event_type=self.event_name.get())
        except ValueError as error:
            print(f"F21SCCW2: error: {error}", file=sys.stderr)
            _ = showerror("Model error", str(error))

    @override
    def go_to(self):
        self.init()
        super().go_to()


class ViewByMainBrowser(PopUp):

    def __init__(self, parent: tk.Frame, window: Window):
        super().__init__(parent, window, "View by Main Browser")

        _ = self.columnconfigure(0, weight=1)
        _ = self.columnconfigure(1, weight=4)

        self.inited: bool = False

        # The menu of event type
        label = tk.Label(self, text="Event type")
        label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.event_name: tk.StringVar = tk.StringVar()

        # The buttons
        view_by_main_browser_button = tk.Button(
            self, text="Ok", command=self.view_by_main_browser_clicked
        )
        view_by_main_browser_button.grid(row=1, column=1, ipadx=10, pady=5)

    def init(self):
        if not self.inited:
            try:
                options = (
                    self.window.cnt._model.event_type_unique()
                )
            except ValueError as error:
                print(f"F21SCCW2: error: {error}", file=sys.stderr)
                _ = showerror("Model error", str(error))
            else:
                event_optionMenu = tk.OptionMenu(self, self.event_name, *options)
                event_optionMenu.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=5)
                self.inited = True


    def view_by_main_browser_clicked(self):
        self.init()
        try:
            self.window.cnt.view_by_browser_graph(event_type=self.event_name.get())
        except ValueError as error:
            print(f"F21SCCW2: error: {error}", file=sys.stderr)
            _ = showerror("Model error", str(error))

    @override
    def go_to(self):
        self.init()
        super().go_to()


class ReaderProfiles(PopUp):
    def __init__(self, parent: tk.Frame, window: Window):
        super().__init__(parent, window, "Reader Profiles")

        # GUI column design
        _ = self.columnconfigure(0, weight=1)
        _ = self.columnconfigure(1, weight=1)

        btn_text = tk.Button(self, text="Render", command=self.on_btn_text_clicked)
        btn_text.grid(row=0, column=0, ipadx=10, pady=5)

        btn_graph = tk.Button(
            self, text="Generate graph", command=self.on_btn_graph_clicked
        )
        btn_graph.grid(row=0, column=1, ipadx=10, pady=5)

        self.text: tk.Text = tk.Text(self, height=10)
        self.text.insert(tk.INSERT, "")
        self.text.grid(row=1, column=0, columnspan=2, sticky=tk.NSEW, padx=5, pady=5)

        # create a Scrollbar and associate it with txt
        scrollb = ttk.Scrollbar(self, command=self.text.yview)
        scrollb.grid(row=1, column=2, sticky=tk.NSEW)
        self.text["yscrollcommand"] = scrollb.set

    def on_btn_text_clicked(self):
        try:
            s = self.window.cnt.reader_profile_text()
        except ValueError as error:
            print(f"F21SCCW2: error: {error}", file=sys.stderr)
            _ = showerror("Model error", str(error))
        else:
            self.text.delete("1.0", tk.END)
            self.text.insert(tk.INSERT, s)
            self.text.update()

    def on_btn_graph_clicked(self):
        try:
            self.window.cnt.reader_profile_graph()
        except ValueError as error:
            print(f"F21SCCW2: error: {error}", file=sys.stderr)
            _ = showerror("Model error", str(error))

    @override
    def go_to(self):
        super().go_to()


class AlsoLikes(PopUp):
    def __init__(self, parent: tk.Frame, window: Window):
        super().__init__(parent, window, "Also Likes")

        # GUI column design
        _ = self.columnconfigure(0, weight=1)
        _ = self.columnconfigure(1, weight=1)

        # The input boxes
        label = tk.Label(self, text="Document UUID")
        label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.docID: tk.StringVar = tk.StringVar()  # store docID value
        docID_entry = tk.Entry(self, textvariable=self.docID)
        docID_entry.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=5)

        label = tk.Label(self, text="User UUID")
        label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.userID: tk.StringVar = tk.StringVar()  # store userID value
        userID_entry = tk.Entry(self, textvariable=self.userID)
        userID_entry.grid(row=1, column=1, sticky=tk.EW, padx=5, pady=5)

        # The buttons
        also_likes_button = tk.Button(
            self, text="Render", command=self.also_like_clicked_text
        )
        also_likes_button.grid(row=2, column=0, ipadx=10, pady=5)
        also_likes_generate_graph = tk.Button(
            self, text="Generate graph", command=self.also_likes_generate_graph_clicked
        )
        also_likes_generate_graph.grid(row=2, column=1, ipadx=10, pady=5)

        # Textbox
        self.text: tk.Text = tk.Text(self, height=10)
        self.text.insert(tk.INSERT, "")
        self.text.grid(row=3, column=0, columnspan=2, sticky=tk.NSEW, padx=5, pady=5)

        # create a Scrollbar and associate it with txt
        scrollb = ttk.Scrollbar(self, command=self.text.yview)
        scrollb.grid(row=3, column=2, sticky=tk.NSEW)
        self.text["yscrollcommand"] = scrollb.set

    def also_like_clicked_text(self):
        try:
            s = self.window.cnt.also_like_text(
                docID=self.docID.get(), userID=self.userID.get()
            )
        except ValueError as error:
            print(f"F21SCCW2: error: {error}", file=sys.stderr)
            _ = showerror("Model error", str(error))
        except GraphvizError as error:
            print(f"F21SCCW2: error: {error}", file=sys.stderr)
            _ = showerror("Graphviz error", str(error))
        else:
            self.text.delete("1.0", tk.END)
            self.text.insert(tk.INSERT, s)
            self.text.update()

    def also_likes_generate_graph_clicked(self):
        try:
            self.window.cnt.also_like_graph(
                docID=self.docID.get(), userID=self.userID.get()
            )
        except ValueError as error:
            print(f"F21SCCW2: error: {error}", file=sys.stderr)
            _ = showerror("Model error", str(error))
        except GraphvizError as error:
            print(f"F21SCCW2: error: {error}", file=sys.stderr)
            _ = showerror("Graphviz error", str(error))

    @override
    def go_to(self):
        super().go_to()


if __name__ == "__main__":
    import os

    mdl = Model()
    cnt = Controller(mdl)
    cnt.load_file(
        os.path.join(os.path.dirname(__file__), "..", "samples", "sample_small.json")
    )
    win = Window(cnt)
    win.mainloop()
