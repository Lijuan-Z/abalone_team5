"""Made up of the DisplayClass and the LogicalClass for Game."""
import tkinter as tk

from gui.refactor_game.game_display_state import GameDisplayState
from gui.refactor_game.game_logical_state import GameLogicalState

class GamePage(tk.Frame):
    """Parent tkinter frame that ties the logical and display classes."""

    def __init__(self, parent, config, back_to_config_callback, **kwargs):
        super().__init__(parent)
        # self.configure(background="white")
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.default_config = config

        self.logical_state = GameLogicalState(parent=self, config=config, back_to_config_callback=back_to_config_callback, **kwargs)

        self.display_state = (
            GameDisplayState(
                parent=parent,
                observed_logical_state=self.logical_state
            )
        )

        self.logical_state.bind_display(self.display_state)

        self.display_state.grid(row=0, column=0, sticky="nsew")

        self.display_state.board.update_board()
        self.display_state.top_info.update_labels()
        self.display_state.side_info.dynamic_init()
