"""Responsible for displaying via tkinter and exposing for display updates."""

import tkinter as tk

from gui.refactor_game.widget.board import Board
from gui.refactor_game.widget.bottom_bar import BottomBar
from gui.refactor_game.widget.side_info import SideInfo
from gui.refactor_game.widget.top_info import TopInfo


class GameDisplayState(tk.Frame):
    """Stores and displays the display state of the config page.

    Display state is state of the 'frontend'
    """

    def __init__(self, parent, observed_logical_state, **kwargs):
        super().__init__(parent)
        self.parent = parent

        self.observed_logical_state = observed_logical_state

        self.top_info = TopInfo(parent=self,
                                bg='blue', width=1, height=1,
                                **kwargs)

        self.board = Board(parent=self,
                           bg='red', width=1, height=1,
                           **kwargs)

        self.side_info = SideInfo(parent=self,
                                  bg='green', width=1, height=1,
                                  **kwargs)

        self.bottom_bar = BottomBar(parent=self,
                                    bg='purple', width=1, height=1,
                                    **kwargs)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=10)
        self.rowconfigure(2, weight=1)

        self.columnconfigure(0, weight=5)
        self.columnconfigure(1, weight=4)

        self.top_info.grid(row=0, column=0, rowspan=1, columnspan=2,
                           sticky='nsew', padx=20, pady=20)

        self.board.grid(row=1, column=0, rowspan=1, columnspan=1,
                        sticky='nsew', padx=50, pady=20)

        self.side_info.grid(row=1, column=1, rowspan=1, columnspan=1,
                            sticky='nsew', padx=20, pady=20)

        self.bottom_bar.grid(row=2, column=0, rowspan=1, columnspan=2,
                             sticky='nsew', padx=20, pady=20)

    def bind_logical_state(self, state):
        self.observed_logical_state = state



