import tkinter as tk
from View.main_style import get_theme

class BinIODefault:
    def __init__(self, parent, binio_name='',x_position=0, y_position=0):
        self.parent = parent
        self.style = get_theme()
        self.frame = tk.LabelFrame(parent,
                                 text=binio_name,
                                 bg="red",
                                 width=100,
                                 height=100,
                                 borderwidth=2,
                                 relief="groove")
        
        # Store initial position
        self.x = x_position
        self.y = y_position
        
        # Bind mouse events
        self.frame.bind("<ButtonPress-1>", self.start_drag)
        self.frame.bind("<B1-Motion>", self.on_drag)
        self.frame.bind("<ButtonRelease-1>", self.stop_drag)
        
        self.frame.place(x=500, y=200)  # Default position
    
    def start_drag(self, event):
        # Store initial mouse position and widget position
        self._drag_data = {"x": event.x, "y": event.y}
        self.frame.configure(relief="sunken")
    
    def on_drag(self, event):
        # Calculate how much the mouse moved
        delta_x = event.x - self._drag_data["x"]
        delta_y = event.y - self._drag_data["y"]
        
        # Get current position
        x = self.frame.winfo_x() + delta_x
        y = self.frame.winfo_y() + delta_y
        
        # Move the widget
        self.frame.place(x=x, y=y)
        
        # Update the drag data for the next motion event
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y
    
    def stop_drag(self, event):
        self.frame.configure(relief="groove")
        if hasattr(self, '_drag_data'):
            del self._drag_data
