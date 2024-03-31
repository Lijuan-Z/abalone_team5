import tkinter as tk
from tkinter import ttk


class ConfigPage(tk.Frame):
    """Config page"""
    def __init__(self, parent, next_page_callback, **kwargs):
        super().__init__(parent)
        self.parent = parent
        self.start_game_callback = next_page_callback

        # dictionary of components
        self.comps = {}

        # dictionary of variables
        self.vars = {}

        self.pack_difficulty_dropdown()
        self.pack_start_game_dropdown()

    def pack_start_game_dropdown(self):
        """Packs the start game button."""
        start_button = tk.Button(self, text="Start Game",
                                 command=self.call_start_game_callback)
        self.comps['start_button'] = start_button
        self.comps['start_button'].pack(pady=10)

    def pack_difficulty_dropdown(self):
        """Packs the difficulty dropdown."""
        self.vars['difficulty'] = tk.StringVar()
        dropdown = ttk.Combobox(self,
                                textvariable=
                                self.vars['difficulty'],
                                values=["Easy", "Medium",
                                        "Hard"],)

        self.comps['difficulty_dropdown'] = dropdown
        self.comps['difficulty_dropdown'].pack(pady=10)

    def call_start_game_callback(self):
        """Handles the calling of the start_game_callback function.

        The Button callbacks only let you put in a single command with no
        arguments so the arguments need to be handled by an external function
        like this
        """
        difficulty = self.vars['difficulty'].get()
        self.start_game_callback(difficulty)
