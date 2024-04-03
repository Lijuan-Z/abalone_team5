"""Made up of the DisplayClass and the LogicalClass for Game."""
import tkinter as tk

from gui.refactor_game.game_display_state import GameDisplayState
from gui.refactor_game.game_logical_state import GameLogicalState

class GamePage(tk.Frame):
    """Parent tkinter frame that ties the logical and display classes."""

    def __init__(self, parent, config, **kwargs):
        super().__init__(parent)
        # self.configure(background="white")
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.default_config = config

        self.logical_state = GameLogicalState(config=config)

        self.display_state = (
            GameDisplayState(parent=parent,
                             get_top_info_callback=self.logical_state.get_top_info,
                             get_board_callback=self.logical_state.get_board,
                             handle_start_callback=self.logical_state.handle_start_callback,
                             handle_input_confirm_callback=self.logical_state.handle_input_confirm_callback,
                             handle_pause_callback=self.logical_state.handle_pause_callback,
                             handle_resume_callback=self.logical_state.handle_resume_callback,
                             handle_undo_last_move_callback=self.logical_state.handle_undo_last_move_callback,
                             handle_reset_callback=self.logical_state.handle_reset_callback,
                             handle_stop_callback=self.logical_state.handle_stop_callback,
                             )
        )
        self.display_state.grid(row=0, column=0, sticky="nsew")

        self.display_state.board_widget.update_board(self.logical_state.board)
