from tkinter import *
import tkinter.ttk as ttk
from View.main_style import get_theme
from View.individual_surfaces.mapping_view import MappingView


class MainView(Tk):
    """
    Class MainView:
    This class is used to create the main window of MOSTwo. It is a subclass of Tk and uses the Notebook class to create a tabbed interface.
    """

    def __init__(self):
        # main setup
        super().__init__()
        self.title('MOSTwo')
        self.geometry("1000x800")
        self.style = get_theme()

        # widgets
        self.notebook = Notebook(self)

        # run it
        self.mainloop()


class Notebook():

    def __init__(self, parent):
        # general setup
        self.parent = parent
        self.notebook = ttk.Notebook(self.parent)
        self.notebook.pack(fill="both", expand=True)
        self.style = get_theme()

        # set common properties for tabs
        self.tab_names = ["Inputs", "Outputs", "Hardware", "Mapping"]

        # add tabs to frame and create collection of tabs
        self.tabs = {}
        for tab_name in self.tab_names:
            tab = ttk.Frame(self.notebook)
            self.notebook.add(tab, text=tab_name)
            self.tabs[tab_name] = tab

        # create instances of tabs
        self.mapping_view = MappingView(self.tabs["Mapping"])

    def get_tab_frame(self, tab_name):
        return self.tabs.get(tab_name, None)
