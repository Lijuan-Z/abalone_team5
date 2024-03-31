import tkinter as tk
from tkinter import ttk

class GamePage(tk.Frame):
    def __init__(self, parent, difficulty):
        super().__init__(parent)
        self.difficulty = difficulty

        # dictionary of components
        self.comps = {}

        # dictionary of variables
        self.vars = {}

        self.pack_message_label()

    def pack_message_label(self):
        """Packs the message label."""
        message_label = tk.Label(self,
                                 text=f"Game started on "
                                      f"{self.difficulty} difficulty!")
        self.comps['message_label'] = message_label
        self.comps['message_label'].pack(pady=20)
