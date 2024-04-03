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

    def __init__(self, parent,
                 get_top_info_callback,
                 get_board_callback,
                 handle_start_callback,
                 handle_input_confirm_callback,
                 handle_pause_callback,
                 handle_resume_callback,
                 handle_undo_last_move_callback,
                 handle_reset_callback,
                 handle_stop_callback,
                 **kwargs):
        super().__init__(parent)
        self.parent = parent

        self.top_info = TopInfo(self, bg='blue', width=1, height=1,
                                     get_top_info_callback=get_top_info_callback,
                                     **kwargs)
        self.board_widget = (
            Board(self, bg='red', width=1, height=1,
                             get_board_callback=get_board_callback,
                             **kwargs)
        )

        self.side_info = SideInfo(self, bg='green', width=1,
                                       height=1, **kwargs)
        self.bottom_bar = BottomBar(self, bg='purple', width=1,
                                         height=1,
                                         update_labels_callback=self.top_info.update_labels,
                                         update_board_callback=self.board_widget.update_board,
                                         handle_start_callback=handle_start_callback,
                                         handle_input_confirm_callback=handle_input_confirm_callback,
                                         handle_pause_callback=handle_pause_callback,
                                         handle_resume_callback=handle_resume_callback,
                                         handle_undo_last_move_callback=handle_undo_last_move_callback,
                                         handle_reset_callback=handle_reset_callback,
                                         handle_stop_callback=handle_stop_callback,
                                         **kwargs)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=10)
        self.rowconfigure(2, weight=1)

        self.columnconfigure(0, weight=5)
        self.columnconfigure(1, weight=4)

        self.top_info.grid(row=0, column=0, rowspan=1, columnspan=2,
                           sticky='nsew', padx=20, pady=20)
        self.board_widget.grid(row=1, column=0, rowspan=1, columnspan=1,
                               sticky='nsew', padx=50, pady=20)
        self.side_info.grid(row=1, column=1, rowspan=1, columnspan=1,
                            sticky='nsew', padx=20, pady=20)
        self.bottom_bar.grid(row=2, column=0, rowspan=1, columnspan=2,
                             sticky='nsew', padx=20, pady=20)


