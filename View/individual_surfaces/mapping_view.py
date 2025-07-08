import tkinter as tk
from View.main_style import get_theme
from View.binio_frames.binio_view_default import BinIODefault
from Model.internal_IO.clock_IO import Clock_IO


class MappingView:
    def __init__(self, parent):
        self.parent = parent
        self.style = get_theme()
        self.my_canvas = tk.Canvas(self.parent, bg="grey")  # surface for mapping
        self.my_canvas.pack(fill="both", expand=True)

        # test initialization of generic binio, has to be done by instance of bin_io
        # my_binio = BinIODefault(self.my_canvas, 'test-tile', 100, 100)
        timer_test = Clock_IO(name="test_clock", target_time="19:55", days_of_week=[0, 1, 2, 3, 4, 5, 6], mapping_view=self)
        # timer_test._create_mapping_tile(self, name="test_clock")

    def get_mappingview(self):
        return self.my_canvas
