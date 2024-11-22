import tkinter as tk


# root window
# root = tk.Tk()
# root.title("GUI")
# root.geometry("600x400+50+50")



# # Frames
# inputs_frame = tk.Frame(root)
# inputs_frame.pack(padx = 10, pady = 10, fill = 'x', expand = True)
# buttons_frame = tk.Frame(root)
# buttons_frame.pack(padx = 10, pady = 10, fill = 'x', expand = True)

# # The input boxes
# docID = tk.StringVar() # store docID value
# userID = tk.StringVar() # store userID value
# docID_entry = tk.Entry(inputs_frame, textvariable=docID)
# userID_entry = tk.Entry(inputs_frame, textvariable=userID)
# docID_entry.pack(fill = 'x', expand = True)
# userID_entry.pack(fill = 'x', expand = True)

# # The buttons
# view_by_country_button = tk.Button(buttons_frame, text="View by country", command = "view_by_country_clicked")
# view_by_country_button.pack(fill='x', expand = True, pady = 10)

# The histogram/result display

# root.mainloop()

class Window(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Home")
        self.geometry("340x200")


        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        menu = tk.Menu(self)
        menu_i = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Features", menu=menu_i)

        for f in (BlankPage, ViewByCountryPage, ViewByContinentPage, ViewByBrowser, ViewByMainBrowser, ReaderProfiles, AlsoLikes):
            self.frames[f] = f(container, self)
            self.frames[f].grid(row=0, column=0, stick="nsew")
            menu_i.add_command(label=self.frames[f].page_name, command=self.frames[f].go_to)

        self.select_frame(ViewByCountryPage)
        self.config(menu=menu)

    def select_frame(self, frame):
        self.frames[frame].tkraise()

class PopUp(tk.Frame):
    def __init__(self, parent, window):
        self.window = window
        super().__init__(parent)

    def go_to(self):
        self.window.select_frame(type(self))
        self.window.title(self.page_name)  

# The Home page (blank)
class BlankPage(PopUp):

    def __init__(self, parent, window):
        super().__init__(parent, window)
        self.page_name = "Home"

    def go_to(self):
        super().go_to()

# The view by country page
class ViewByCountryPage(PopUp):
    
    def __init__(self, parent, window):
        super().__init__(parent, window)
        self.page_name = "View by Country"
        
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=4)

        # The input boxes
        label = tk.Label(self, text = "Document UUID")
        label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.docID = tk.StringVar() # store docID value
        docID_entry = tk.Entry(self, textvariable=self.docID)
        docID_entry.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=5)

        # The buttons
        view_by_country_button = tk.Button(self, text="Ok", command = "view_by_country_clicked")
        view_by_country_button.grid(row=1, column=1, ipadx=10, pady=5)

    def go_to(self):
        super().go_to()

# The view by continent page
class ViewByContinentPage(PopUp):

    def __init__(self, parent, window):
        super().__init__(parent, window)
        self.page_name = "View by Continent"
        
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=4)

        # The input boxes
        label = tk.Label(self, text = "Document UUID")
        label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.docID = tk.StringVar() # store docID value
        docID_entry = tk.Entry(self, textvariable=self.docID)
        docID_entry.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=5)

        # The buttons
        view_by_continent_button = tk.Button(self, text="Ok", command="view_by_continent_clicked")
        view_by_continent_button.grid(row=1, column=1, ipadx=10, pady=5)

    def go_to(self):
        super().go_to()

class ViewByBrowser(PopUp):

    def __init__(self, parent, window):
        super().__init__(parent, window)
        self.page_name = "View by Browser"
        
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=4)

        # The menu of event type
        label = tk.Label(self, text = "Event type")
        label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        event_name = tk.StringVar()
        options = ["a", "b", "c"] #CHANGE THIS ONEEEEEEEE TO A METHOD THAT RECEIVE EVENT TYPE FROM MODEL.PY!!!!!!!!!!!!!
        event_optionMenu = tk.OptionMenu(self, event_name, *options)
        event_optionMenu.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=5)

        # The buttons
        view_by_browser_button = tk.Button(self, text="Ok", command="view_by_browser_clicked")
        view_by_browser_button.grid(row=1, column=1, ipadx=10, pady=5)
    
    def go_to(self):
        super().go_to()

class ViewByMainBrowser(PopUp):

    def __init__(self, parent, window):
        super().__init__(parent, window)
        self.page_name = "View by Main Browser"
        
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=4)

        # The menu of event type
        label = tk.Label(self, text = "Event type")
        label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        event_name = tk.StringVar()
        options = ["a", "b", "c"] #CHANGE THIS ONEEEEEEEE TO A METHOD THAT RECEIVE EVENT TYPE FROM MODEL.PY!!!!!!!!!!!!!
        event_optionMenu = tk.OptionMenu(self, event_name, *options)
        event_optionMenu.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=5)

        # The buttons
        view_by_main_browser_button = tk.Button(self, text="Ok", command="view_by_main_browser_clicked")
        view_by_main_browser_button.grid(row=1, column=1, ipadx=10, pady=5)
    
    def go_to(self):
        super().go_to()

class ReaderProfiles(PopUp):

    def __init__(self, parent, window):
        super().__init__(parent, window)
        self.page_name = "Reader Profiles"

        # Add method to load reader profile from Model.py

    def go_to(self):
        super().go_to()

class AlsoLikes(PopUp):

    def __init__(self, parent, window):
        super().__init__(parent, window)
        self.page_name = "Also Likes"

        # GUI column design
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=4)

        # The input boxes
        label = tk.Label(self, text = "Document UUID")
        label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.docID = tk.StringVar() # store docID value
        docID_entry = tk.Entry(self, textvariable=self.docID)
        docID_entry.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=5)

        # The buttons
        also_likes_button = tk.Button(self, text="Ok", command="also_likes_clicked")
        also_likes_button.grid(row=1, column=1, ipadx=10, pady=5)
        also_likes_generate_graph = tk.Button(self, text="Generate graph", command="also_likes_generate_graph_clicked")
        also_likes_generate_graph.grid(row=2, column=1, ipadx=10, pady=5)

    def go_to(self):
        super().go_to()

win = Window()
win.mainloop()