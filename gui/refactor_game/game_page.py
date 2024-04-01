import tkinter as tk
from enum import Enum
from tkinter import ttk
from gui.refactor_game.config_page import Color


class Player():
    """Represents a player."""
    ONE = 0
    TWO = 1

    def __init__(self, color, operator, turn_time, turns_left):
        self.color = color
        self.operator = operator
        self.turn_time = turn_time
        self.turns_left = turns_left
        self.time_left = None if turn_time is None else tk.IntVar(turn_time)

class GameLogicalState:
    """Stores and mutates the logical state of the game.

    Logical state is state of the 'backend'
    """
    def __init__(self, config, **kwargs):
        self.config = config

        self.players = {
            Player.ONE: Player(
                color=config['player_1_color'],
                operator=config['player_1_operator'],
                turn_time=config['player_1_seconds_per_turn'],
                turns_left=config['player_1_turn_limit'],
            ),
            Player.TWO: Player(
                color=config['player_2_color'],
                operator=config['player_2_operator'],
                turn_time=config['player_2_seconds_per_turn'],
                turns_left=config['player_2_turn_limit']
            )
        }

        self.current_player = (
            Player.ONE if self.players[Player.ONE].color == Color.BLACK
            else Player.TWO
        )
        self.next_player = (
            Player.TWO if (self.players[Player.TWO]).color == Color.WHITE
            else Player.ONE
        )


class GameDisplayState(tk.Frame):
    """Stores and displays the display state of the config page.

    Display state is state of the 'frontend'
    """
    def __init__(self, parent, **kwargs):
        super().__init__(parent)
        self.parent = parent

        # dictionary of components
        self.comps = {}

        # dictionary of variables
        self.vars = {}

class GamePage(tk.Frame):
    def __init__(self, parent, config):
        super().__init__(parent)
        self.default_config = config

        self.display_state = GameDisplayState(parent=parent, **config)
        self.display_state.pack(expand=True, anchor=tk.CENTER)

        self.logical_state = GameLogicalState(**config)
