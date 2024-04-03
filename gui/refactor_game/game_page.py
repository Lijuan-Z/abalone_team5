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

class LogItem():
    def __init__(self, move, result_board, time_taken):
        self.move = move
        self.board = result_board
        self.time_taken = time_taken

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
        self.score = 0
        self.log = []


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

        self.one_second_pass_timer = None

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

        self.game_state = "NO GAME STARTED"

    def get_board(self):
        """Returns the board.

        :rtype: dict[int, int]
        """
        return self.board

    def get_top_info(self):
        """Returns the information needed for the top info widget"""
        player_1 = self.players[Player.ONE]
        player_2 = self.players[Player.TWO]
        info = {
            'game_state': self.game_state,
            'cur_player': f"{'Player_1' if self.current_player == Player.ONE else 'Player_2'}({self.players[self.current_player].color})",
            'player_1_marble_color': player_1.color,
            'player_1_turns_left': player_1.turns_left if player_1.turns_left is not None else "Unlimited",
            'player_1_score': player_1.score,
            'player_1_time_left': player_1.time_left.get() if player_1.time_left is not None else "Unlimited",
            'player_2_marble_color': player_2.color,
            'player_2_turns_left': player_2.turns_left if player_2.turns_left is not None else "Unlimited",
            'player_2_score': player_2.score,
            'player_2_time_left': player_2.time_left.get() if player_2.time_left is not None else "Unlimited"
        }

        return info

    def swap_players(self):
        self.current_player, self.next_player = self.next_player, self.current_player

    def execute_string_input(self, action_string, update_board_callback):
        origin_half, destination_half = action_string.split('-')

        origin_coord_strings = [origin_half[(i - 1) * 2:2 * i]for i in range(int(len(origin_half) / 2), 0, -1)]
        destination_coord_strings = [destination_half[(i - 1) * 2:2 * i]for i in range(int(len(destination_half) / 2), 0, -1)]

        for origin_coord_string, destination_coord_string in zip(origin_coord_strings, destination_coord_strings):
            origin_column_digit = (ord(origin_coord_string[0].upper()) - 64)
            origin_row_digit = int(origin_coord_string[1])

            destination_column_digit = (ord(destination_coord_string[0].upper()) - 64)
            destination_row_digit = int(destination_coord_string[1])

            marble_color = self.board[origin_column_digit*10 + origin_row_digit]
            del self.board[origin_column_digit*10 + origin_row_digit]
            self.board[destination_column_digit*10 + destination_row_digit] = marble_color




        # for coord in line.split(',', ):
        #     coord = coord[0].upper() + coord[1:]
        #     column_digit = (ord(coord[0]) - 64)
        #     row_digit = int(coord[1])
        #     color = 0 if coord[2] == 'b' else 1
        #     board[column_digit*10 + row_digit] = color
        update_board_callback(self.board)


    def handle_start_callback(self, caller):
        """Handles start button."""
        print("start")
        pass

    def handle_input_confirm_callback(self, user_input, update_board_callback, update_labels_callback):
        """Handles action input confirm event."""
        print("input confirm")
        print(f"user_input: {user_input}")
        self.execute_string_input(
            action_string=user_input,
            update_board_callback=update_board_callback
        )
        cur_player = self.players[self.current_player]
        new_log = LogItem(user_input,
                          self.board.copy,
                          cur_player.time_left.get() - cur_player.turn_time)
        cur_player.log.append(new_log)
        cur_player.time_left.set(cur_player.turn_time)
        cur_player.turns_left -= 1
        self.swap_players()
        update_labels_callback()
        pass

    def handle_pause_callback(self):
        """Handles pause button."""
        print("pause")
        pass

    def handle_resume_callback(self):
        """Handles resume button."""
        print("resume")
        pass

    def handle_undo_last_move_callback(self):
        """Handles undo last move button."""
        print("undo")
        pass

    def handle_reset_callback(self):
        """Handles reset button."""
        print("reset")
        pass

    def handle_stop_callback(self):
        """Handles stop button."""
        print("stop")
        pass


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

        self.top_info = self.TopInfo(self, bg='blue', width=1, height=1,
                                     get_top_info_callback=get_top_info_callback,
                                     **kwargs)
        self.board_widget = (
            self.BoardWidget(self, bg='red', width=1, height=1,
                             get_board_callback=get_board_callback,
                             **kwargs)
        )

        self.side_info = self.SideInfo(self, bg='green', width=1,
                                       height=1, **kwargs)
        self.bottom_bar = self.BottomBar(self, bg='purple', width=1,
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

    class TopInfo(tk.Frame):
        """Contains information like score, turns remaining, etc."""

        def __init__(self, parent, get_top_info_callback, *args, **kwargs):
            super().__init__(parent, **kwargs)
            self.get_top_info_callback = get_top_info_callback

            self.rowconfigure(0, weight=1)
            self.rowconfigure(1, weight=1)

            self.columnconfigure(0, weight=4)
            self.columnconfigure((1, 2, 3, 4, 5), weight=1)
            self.columnconfigure(6, weight=4)

            self.game_state_label = tk.Label(self, text="")
            self.cur_player_label = tk.Label(self, text="")
            self.player_1_marble_color_label = tk.Label(self, text="")
            self.player_1_turns_left_label = tk.Label(self, text="")
            self.player_1_score_label = tk.Label(self, text="")
            self.player_1_time_left_label = tk.Label(self, text="")
            self.player_2_marble_color_label = tk.Label(self, text="")
            self.player_2_turns_left_label = tk.Label(self, text="")
            self.player_2_score_label = tk.Label(self, text="")
            self.player_2_time_left_label = tk.Label(self, text="")

            self.game_state_label.grid(row=0, column=1)
            self.cur_player_label.grid(row=1, column=1)
            self.player_1_marble_color_label.grid(row=0, column=2)
            self.player_1_turns_left_label.grid(row=0, column=3)
            self.player_1_score_label.grid(row=0, column=4)
            self.player_1_time_left_label.grid(row=0, column=5)
            self.player_2_marble_color_label.grid(row=1, column=2)
            self.player_2_turns_left_label.grid(row=1, column=3)
            self.player_2_score_label.grid(row=1, column=4)
            self.player_2_time_left_label.grid(row=1, column=5)

            self.update_labels()


        def update_labels(self):
            info = self.get_top_info_callback()
            self.set_labels(**info)

        def set_labels(self,
                       game_state,
                       cur_player,
                       player_1_marble_color,
                       player_1_turns_left,
                       player_1_score,
                       player_1_time_left,
                       player_2_marble_color,
                       player_2_turns_left,
                       player_2_score,
                       player_2_time_left,
                       **kwargs):
            self.game_state_label.config(text=f'game state: {game_state}')
            self.cur_player_label.config(text=f'cur player: {cur_player}')
            self.player_1_marble_color_label.config(text=f'player 1 marble_color: {player_1_marble_color}')
            self.player_1_turns_left_label.config(text=f'player 1 turns_left: {player_1_turns_left}')
            self.player_1_score_label.config(text=f'player 1 score: {player_1_score}')
            self.player_1_time_left_label.config(text=f'player 1 time_left: {player_1_time_left}')
            self.player_2_marble_color_label.config(text=f'player 2 marble_color: {player_2_marble_color}')
            self.player_2_turns_left_label.config(text=f'player 2 turns_left: {player_2_turns_left}')
            self.player_2_score_label.config(text=f'player 2 score: {player_2_score}')
            self.player_2_time_left_label.config(text=f'player 2 time_left: {player_2_time_left}')






    class BoardWidget(tk.Frame):
        """Displays the game board."""
        CIRCLE_RADIUS = 30
        COLUMNS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']

        def __init__(self, parent,
                     get_board_callback,
                     *args, **kwargs):
            super().__init__(parent, **kwargs)
            self.canvas = tk.Canvas(self, bg="pink")
            self.canvas.bind("<Button-1>", lambda event: print(f'{event.x}:{event.y}'))

            self.columnconfigure(0, weight=1)
            self.rowconfigure(0, weight=1)

            self.canvas.grid(row=0, column=0, sticky='nsew')
            self.bind("<Configure>",
                      lambda event: self.update_board(
                          get_board_callback()
                      ))

        def click_coord_to_marble_coord(self, coord):
            pass

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

                        color_value = '#7E7E7E'
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

        def __init__(self, parent,
                     update_labels_callback,
                     update_board_callback,
                     handle_start_callback,
                     handle_input_confirm_callback,
                     handle_pause_callback,
                     handle_resume_callback,
                     handle_undo_last_move_callback,
                     handle_reset_callback,
                     handle_stop_callback,
                     *args, **kwargs):
            super().__init__(parent, **kwargs)

            self.rowconfigure(0, weight=1)

            self.columnconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)

            # start
            self.start_button = tk.Button(self, text='Start', command=handle_start_callback)
            self.start_button.grid(row=0, column=0)

            # input action
            self.input_action_entry = tk.Entry(self)
            self.input_action_entry.insert(0, 'Enter your action...')
            self.input_action_entry.bind('<FocusIn>', lambda event: self.input_action_entry.delete(0, 'end'))

            def input_confirm(event):
                handle_input_confirm_callback(user_input=self.input_action_entry.get(), update_board_callback=update_board_callback, update_labels_callback=update_labels_callback)
                self.input_action_entry.delete(0, 'end')

            self.input_action_entry.bind('<Return>', lambda event: input_confirm(event))
            self.input_action_entry.grid(row=0, column=1)

            # pause
            self.pause_button = tk.Button(self, text='Pause', command=handle_pause_callback)
            self.pause_button.grid(row=0, column=2)

            # resume
            self.resume_button = tk.Button(self, text='Resume', command=handle_resume_callback)
            self.resume_button.grid(row=0, column=3)

            # undo last move
            self.undo_last_move_button = tk.Button(self, text='Undo Last Move', command=handle_undo_last_move_callback)
            self.undo_last_move_button.grid(row=0, column=4)

            # reset
            self.reset_button = tk.Button(self, text='Reset', command=handle_reset_callback)
            self.reset_button.grid(row=0, column=5)

            # stop
            self.stop_button = tk.Button(self, text='Stop', command=handle_stop_callback)
            self.stop_button.grid(row=0, column=6)


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
