import tkinter as tk
from View.main_style import get_theme

# we create an instance of this tile for every binio instance. have to add properties etc.
class BinIODefault:
    def __init__(self, parent):
        self.parent = parent
        self.style = get_theme()
        new_frame = tk.LabelFrame(parent,
                                  text='testtext',
                                  bg="red",
                                  width=100,
                                  height=100,
                                  borderwidth=2,
                                  relief="groove")

        new_frame.style = get_theme()
        new_frame.place(x=500, y=200)

