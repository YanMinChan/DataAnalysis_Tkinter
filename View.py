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
        self.title("GUI")
        self.geometry("600x400+50+50")


        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        menu = tk.Menu(self)
        menu_i = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Features", menu=menu_i)

        for f in (BlankPage, ViewByCountryPage, ViewByContinentPage):
            self.frames[f] = f(container, self)
            self.frames[f].grid(row=0, column=0, stick="nsew")
            menu_i.add_command(label=self.frames[f].page_name, command=self.frames[f].go_to)

        self.select_frame(BlankPage)
        self.config(menu=menu)

    def select_frame(self, frame):
        self.frames[frame].tkraise()

class BlankPage(tk.Frame):

    def __init__(self, parent, window):
        self.window = window
        super().__init__(parent)
        self.page_name = "Home"

    def go_to(self):
        self.window.select_frame(type(self))

class ViewByCountryPage(tk.Frame):
    
    def __init__(self, parent, window):
        self.window = window
        super().__init__(parent)
        self.page_name = "View by Country"

        # The input boxes
        label = tk.Label(self, text = "Document UUID")
        label.pack()
        self.docID = tk.StringVar() # store docID value
        self.docID_entry = tk.Entry(self, textvariable=self.docID)
        self.docID_entry.pack(fill = 'x', expand = True, padx = 10)

        # The buttons
        self.view_by_country_button = tk.Button(self, text="Ok", command = "view_by_country_clicked")
        self.view_by_country_button.pack(fill='x', expand = True, pady = 10, padx = 10)

    def go_to(self):
        self.window.select_frame(type(self))

class ViewByContinentPage(tk.Frame):

    def __init__(self, parent, window):
        self.window = window
        super().__init__(parent)
        self.page_name = "View by Continent"

        # The input boxes
        self.docID = tk.StringVar() # store docID value
        self.docID_entry = tk.Entry(self, textvariable=self.docID)
        self.docID_entry.pack(fill = 'x', expand = True)

        # The buttons
        self.view_by_continent_button = tk.Button(self, text="Ok (continent)", command = "view_by_continent_clicked")
        self.view_by_continent_button.pack(fill='x', expand = True, pady = 10)

    def go_to(self):
        self.window.select_frame(type(self))

win = Window()
win.mainloop()