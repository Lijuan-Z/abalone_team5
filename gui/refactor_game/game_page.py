"""Contains the game page.

Made up of the DisplayClass and the LogicalClass

- the display class is responsible for displaying via tkinter and exposing
  methods for other classes to edit it.

- the logical class is responsible for handling the state of the actual game
  and updating the display class
"""
import math
import tkinter as tk
from enum import Enum
from tkinter import ttk
from gui.refactor_game.config_page import Color, Layout, Operator

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
    STARTING_BOARDS = {
        # default
        Layout.STANDARD.value: {11: 0, 12: 0, 13: 0, 14: 0, 15: 0, 21: 0,
                                22: 0, 23: 0, 24: 0, 25: 0, 26: 0, 33: 0,
                                34: 0, 35: 0, 99: 1, 98: 1, 97: 1, 96: 1,
                                95: 1, 89: 1, 88: 1, 87: 1, 86: 1, 85: 1,
                                84: 1, 77: 1, 76: 1, 75: 1},

        # belgian daisy
        Layout.BELGIAN_DAISY.value: {11: 0, 12: 0, 21: 0, 22: 0, 23: 0, 32: 0,
                                     33: 0, 99: 0, 98: 0, 89: 0, 88: 0, 87: 0,
                                     78: 0, 77: 0, 14: 1, 15: 1, 24: 1, 25: 1,
                                     26: 1, 35: 1, 36: 1, 95: 1, 96: 1, 84: 1,
                                     85: 1, 86: 1, 74: 1, 75: 1},

        # german daisy
        Layout.GERMAN_DAISY.value: {21: 0, 22: 0, 31: 0, 32: 0, 33: 0, 42: 0,
                                    43: 0, 67: 0, 68: 0, 77: 0, 78: 0, 79: 0,
                                    88: 0, 89: 0, 25: 1, 26: 1, 35: 1, 36: 1,
                                    37: 1, 46: 1, 47: 1, 63: 1, 64: 1, 73: 1,
                                    74: 1, 75: 1, 84: 1, 85: 1},
    }

    def __init__(self, config, **kwargs):
        if config is None:
            self.config = {'layout': Layout.STANDARD.value,
                           'player_1_color': Color.BLACK.value,
                           'player_1_operator': Operator.HUMAN.value,
                           'player_1_seconds_per_turn': 30,
                           'player_1_turn_limit': 40,
                           'player_2_color': Color.WHITE.value,
                           'player_2_operator': Operator.AI.value,
                           'player_2_seconds_per_turn': None,
                           'player_2_turn_limit': 40}
        else:
            self.config = config

        self.board = self.STARTING_BOARDS[self.config['layout']]

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

    def get_board(self):
        """Returns the board.

        :rtype: dict[int, int]
        """
        return self.board


class GameDisplayState(tk.Frame):
    """Stores and displays the display state of the config page.

    Display state is state of the 'frontend'
    """

    def __init__(self, parent,
                 get_board_callback,
                 **kwargs):
        super().__init__(parent)
        self.parent = parent

        self.top_info = self.TopInfo(self, bg='blue', width=1,
                                     height=1, **kwargs)
        self.board_widget = (
            self.BoardWidget(self, bg='red', width=1, height=1,
                             get_board_callback=get_board_callback,
                             **kwargs)
        )

        self.side_info = self.SideInfo(self, bg='green', width=1,
                                       height=1, **kwargs)
        self.bottom_bar = self.BottomBar(self, bg='purple', width=1,
                                         height=1, **kwargs)

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
        CIRCLE_RADIUS = 30
        COLUMNS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']

        def __init__(self, parent, get_board_callback, *args, **kwargs):
            super().__init__(parent, **kwargs)
            self.canvas = tk.Canvas(self, bg="pink")

            self.columnconfigure(0, weight=1)
            self.rowconfigure(0, weight=1)

            self.canvas.grid(row=0, column=0, sticky='nsew')
            self.bind("<Configure>",
                      lambda event: self.update_board(
                          get_board_callback()
                      ))

        def update_board(self, board: dict[int, int]):
            """Updates the canvas to draw the given board."""
            self.update()

            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()

            r = 0.03 * math.sqrt((canvas_width ** 2) + (canvas_height ** 2))

            board_length = r * 18

            x_offset = (canvas_width / 2) - (board_length / 2)
            y_offset = (canvas_height / 2)

            self.canvas.delete('all')
            for col in range(9):
                for row in range(-4, 5):
                    if abs(row) >= col or col < 9 - abs(row):
                        x = x_offset + (2 * col + 1) * r + abs(row) * r
                        y = y_offset - r * row * math.sqrt(3)

                        color_value = 'lightgrey'
                        text_color = 'black'

                        k = row if row > 0 else 0

                        key = f'{self.COLUMNS[row + 4]}{col + 1 + k}'

                        self.canvas.create_oval(
                            x - r, y - r, x + r, y + r,
                            fill=color_value
                        )

                        self.canvas.create_text(x, y, text=key,
                                                fill=text_color)

                        self.update()

            # print(board.items())
            offsets = [0, 0, 0, 0, 0, 0, 1, 2, 3, 4]
            for coord, color in board.items():
                # row = (coord)-5) // 10
                # col = (coord - 1 - (coord//10)) % 10

                row = ((coord//10) - 5)
                col = ((coord%10) - 1 - offsets[(coord//10)])

                x = x_offset + (2 * col + 1) * r + abs(row) * r
                y = y_offset - r * row * math.sqrt(3)

                color_value = 'black' if color == 0 else 'white'
                text_color = 'white' if color == 0 else 'black'

                self.canvas.create_oval(
                    x - r, y - r, x + r, y + r,
                    fill=color_value
                )

                k = row if row > 0 else 0
                key = f'{self.COLUMNS[row + 4]}{col + 1 + k}'
                self.canvas.create_text(x, y, text=key,
                                        fill=text_color)
                self.update()

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

        self.display_state = (
            GameDisplayState(parent=parent,
                             get_board_callback=self.logical_state.get_board)
        )
        self.display_state.grid(row=0, column=0, sticky="nsew")

        self.display_state.board_widget.update_board(self.logical_state.board)
