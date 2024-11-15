import tkinter as tk

# root window
root = tk.Tk()
root.title("GUI")
root.geometry("600x400+50+50")

# Frames
inputs_frame = tk.Frame(root)
inputs_frame.pack(padx = 10, pady = 10, fill = 'x', expand = True)
buttons_frame = tk.Frame(root)
buttons_frame.pack(padx = 10, pady = 10, fill = 'x', expand = True)

# The input boxes
docID = tk.StringVar() # store docID value
userID = tk.StringVar() # store userID value
docID_entry = tk.Entry(inputs_frame, textvariable=docID)
userID_entry = tk.Entry(inputs_frame, textvariable=userID)
docID_entry.pack(fill = 'x', expand = True)
userID_entry.pack(fill = 'x', expand = True)

# The buttons
view_by_country_button = tk.Button(buttons_frame, text="View by country", command = "view_by_country_clicked")
view_by_country_button.pack(fill='x', expand = True, pady = 10)

# The histogram/result display

root.mainloop()