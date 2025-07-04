import tkinter as tk
from View.main_style import get_theme
from View.binio_frames.binio_view_default import BinIODefault


class MappingView:
    def __init__(self, parent):
        self.parent = parent
        self.style = get_theme()
        self.my_canvas = tk.Canvas(self.parent, bg="grey")
        self.my_canvas.pack(fill="both", expand=True)

        # test initialization of generic binio, has to be done by instance of bin_io
        my_binio = BinIODefault(self.my_canvas)

    def get_mappingview(self):
        return self.my_canvas
