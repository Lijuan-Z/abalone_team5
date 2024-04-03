import tkinter as tk

class SideInfo(tk.Frame):
    """Contains widgets like the p1 log, p2 log, and AI recommendations"""

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, **kwargs)
