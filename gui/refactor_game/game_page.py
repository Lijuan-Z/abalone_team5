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

    class Component(Enum):
        TOP_INFO_WIDGET = 0
        BOARD_WIDGET = 1
        SIDE_INFO_WIDGET = 2
        BOTTOM_BAR_WIDGET = 3

    def __init__(self, parent, **kwargs):
        super().__init__(parent)
        self.parent = parent

        # dictionary of components
        self.comps = {}

        # dictionary of variables
        self.vars = {}

        # self._pack_top_info_widget()
        # self._pack_board_widget()
        # self._pack_side_info_widget()
        # self._pack_bottom_bar_widget()

    def _pack_top_info_widget(self):
        """Packs the widget that contains the game board display."""
        widget = tk.Frame(self, background="red")
        widget.grid(row=0, rowspan=1, column=0, columnspan=1, padx=8, pady=8)
        self.comps[self.Component.TOP_INFO_WIDGET] = widget

    def _pack_board_widget(self):
        """Packs the widget that contains the game board display."""
        widget = tk.Canvas(self, bg="green")
        widget.grid(row=1, rowspan=1, column=1, columnspan=1)
        self.comps[self.Component.BOARD_WIDGET] = widget

    def _pack_side_info_widget(self):
        """Packs the widget that contains the game board display."""
        widget = tk.Canvas(self, bg="blue")
        widget.grid(row=2, rowspan=1, column=2, columnspan=1)
        self.comps[self.Component.SIDE_INFO_WIDGET] = widget

    def _pack_bottom_bar_widget(self):
        """Packs the widget that contains the game board display."""
        widget = tk.Canvas(self, bg="cyan")
        widget.grid(row=3, rowspan=1, column=3, columnspan=1)
        self.comps[self.Component.BOTTOM_BAR_WIDGET] = widget

    def color_overrides(self):
        try:
            self.comps[self.Component.TOP_INFO_WIDGET].configure(
                bg="#FF0F00"
            )
            self.comps[self.Component.BOARD_WIDGET].configure(
                bg="#00FFFF"
            )
            self.comps[self.Component.SIDE_INFO_WIDGET].configure(
                bg="#00FFFF"
            )
            self.comps[self.Component.BOTTOM_BAR_WIDGET].configure(
                bg="#00FFFF"
            )
        except KeyError as e:
            print("Error with override colors in game_page:", e)
        pass


class GamePage(tk.Frame):
    """Parent tkinter frame that ties the logical and display classes."""

    def __init__(self, parent, config, **kwargs):
        super().__init__(parent)
        self.configure(background="red")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        label = tk.Label(self, text="hello", background='cyan', padx=100, pady=100)
        label.grid(padx=390, pady=30, sticky='new')

        # super().configure(background='')
        # self.grid_columnconfigure(0, weight=1)
        # self.grid_columnconfigure(0, weight=1)

        # self.default_config = config

        # self.logical_state = GameLogicalState(config=config)
        #
        # self.display_state = GameDisplayState(parent=parent)
        #
        # self.display_state.grid(row=0, column=0)

    def color_overrides(self):
        return
        self.display_state.color_overrides()
        pass
