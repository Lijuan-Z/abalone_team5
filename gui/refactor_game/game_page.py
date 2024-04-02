"""Contains the game page.

Made up of the DisplayClass and the LogicalClass

- the display class is responsible for displaying via tkinter and exposing
  methods for other classes to edit it.

- the logical class is responsible for handling the state of the actual game
  and updating the display class
"""

import tkinter as tk
from enum import Enum
from tkinter import ttk
from gui.refactor_game.config_page import Color

from pprint import pprint


class Player():
    """Represents a player."""
    ONE = 0
    TWO = 1

    def __init__(self, color, operator, turn_time, turns_left):
        self.color = color
        self.operator = operator
        self.turn_time = turn_time
        self.turns_left = turns_left
        self.time_left = None if turn_time is None else tk.IntVar(None,
                                                                  turn_time)


class GameLogicalState:
    """Stores and mutates the logical state of the game.

    Logical state is state of the 'backend'
    """

    def __init__(self, config, **kwargs):
        if config is None:
            self.config = {'layout': 'Standard',
                           'player_1_color': 'Black',
                           'player_1_operator': 'Human',
                           'player_1_seconds_per_turn': None,
                           'player_1_turn_limit': 40,
                           'player_2_color': 'White',
                           'player_2_operator': 'AI',
                           'player_2_seconds_per_turn': 10,
                           'player_2_turn_limit': 40}
        else:
            self.config = config

        self.turn_timer = None

        self.players = {
            Player.ONE: Player(
                color=self.config['player_1_color'],
                operator=self.config['player_1_operator'],
                turn_time=self.config['player_1_seconds_per_turn'],
                turns_left=self.config['player_1_turn_limit'],
            ),
            Player.TWO: Player(
                color=self.config['player_2_color'],
                operator=self.config['player_2_operator'],
                turn_time=self.config['player_2_seconds_per_turn'],
                turns_left=self.config['player_2_turn_limit']
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

        self.top_info = self.TopInfo(self, bg='blue', width=1, height=1)
        self.board_widget = self.BoardWidget(self, bg='red', width=1, height=1)
        self.side_info = self.SideInfo(self, bg='green', width=1, height=1)
        self.bottom_bar = self.BottomBar(self, bg='purple', width=1, height=1)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=5)
        self.rowconfigure(2, weight=1)

        self.columnconfigure(0, weight=5)
        self.columnconfigure(1, weight=3)

        self.top_info.grid(row=0, column=0, rowspan=1, columnspan=2,
                           sticky='nsew', padx=20, pady=20)
        self.board_widget.grid(row=1, column=0, rowspan=1, columnspan=1,
                               sticky='nsew', padx=20, pady=20)
        self.side_info.grid(row=1, column=1, rowspan=1, columnspan=1,
                            sticky='nsew', padx=20, pady=20)
        self.bottom_bar.grid(row=2, column=0, rowspan=1, columnspan=2,
                             sticky='nsew', padx=20, pady=20)

    class TopInfo(tk.Frame):
        """Contains information like score, turns remaining, etc."""

        def __init__(self, parent, *args, **kwargs):
            super().__init__(parent, **kwargs)

    class BoardWidget(tk.Frame):
        """Displays the game board."""

        def __init__(self, parent, *args, **kwargs):
            super().__init__(parent, **kwargs)

    class SideInfo(tk.Frame):
        """Contains widgets like the p1 log, p2 log, and AI recommendations"""

        def __init__(self, parent, *args, **kwargs):
            super().__init__(parent, **kwargs)

    class BottomBar(tk.Frame):
        """Contains all the buttons and user input fields."""

        def __init__(self, parent, *args, **kwargs):
            super().__init__(parent, **kwargs)


class GamePage(tk.Frame):
    """Parent tkinter frame that ties the logical and display classes."""

    def __init__(self, parent, config, **kwargs):
        super().__init__(parent)
        # self.configure(background="white")
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.default_config = config

        self.logical_state = GameLogicalState(config=config)

        self.display_state = GameDisplayState(parent=parent)
        self.display_state.grid(row=0, column=0, sticky="nsew")
