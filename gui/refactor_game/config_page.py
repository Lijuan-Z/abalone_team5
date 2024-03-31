import tkinter as tk
from tkinter import ttk


class ConfigState(tk.Frame):
    """Stores and provides an interface for the state of the ConfigPage."""

    def __init__(self, parent, next_page_callback, **kwargs):
        super().__init__(parent)

        self.parent = parent
        self.start_game_callback = next_page_callback

        # dictionary of components
        self.comps = {}

        # dictionary of variables
        self.vars = {}

        self._pack_difficulty_dropdown()
        self._pack_start_game_dropdown()

    def _pack_start_game_dropdown(self):
        """Packs the start game button."""

        def button_action():
            """Calls the start game callback and passes difficulty."""
            self.start_game_callback(difficulty=self.vars['difficulty'].get())

        start_button = tk.Button(self,
                                 text="Start Game",
                                 command=button_action)

        self.comps['start_button'] = start_button
        self.comps['start_button'].pack(pady=10)

    def _pack_difficulty_dropdown(self):
        """Packs the difficulty dropdown."""
        self.vars['difficulty'] = tk.StringVar()
        dropdown = ttk.Combobox(self,
                                textvariable=
                                self.vars['difficulty'],
                                values=["Easy", "Medium",
                                        "Hard"])

        self.comps['difficulty_dropdown'] = dropdown
        self.comps['difficulty_dropdown'].pack(pady=10)


class ConfigPage(tk.Frame):
    """Config page"""

    def __init__(self, parent, **kwargs):
        super().__init__(parent)

        self.state = ConfigState(parent=parent, **kwargs)
        self.state.pack()
