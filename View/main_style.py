import tkinter.ttk as ttk

def get_theme() -> ttk.Style:
    my_style = ttk.Style()
    if "yummy" in my_style.theme_names():
        my_style.theme_use("yummy")
        return my_style
    else:
        my_style.theme_create("yummy", parent="alt", settings={
            "TNotebook": {
                "configure": {
                    "tabmargins": [2, 5, 2, 0],
                    "background": "#E0FAF6"
                }
            },
            "TNotebook.Tab": {
                "configure": {
                    "padding": [5, 5],
                    "background": "#B4F2E8",
                    "font": ("Helvetica", 14)
                },
                "map": {
                    "background": [("selected", "#FF999E")],
                    "expand": [("selected", [1, 1, 1, 0])]
                }
            },
            "TFrame": {
                "configure": {
                    "background": "#E4E6EB"
                }
            },
        })
        my_style.theme_use("yummy")
    return my_style