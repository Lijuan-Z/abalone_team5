"""Handles the state of the actual game and triggering updates in display."""
import tkinter as tk

from gui.refactor_game.config_page import Layout, Color, Operator
from gui.refactor_game.data.log import LogItem
from gui.refactor_game.data.player import Player, PlayerFactory


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

    def __init__(self, config, back_to_config_callback, **kwargs):
        self.display_slave = None

        self.back_to_config_callback = back_to_config_callback

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

        self.board = self.STARTING_BOARDS[self.config['layout']].copy()

        self.one_second_pass_timer = None

        self.players = {
            Player.ONE: PlayerFactory.make_player(
                operator=self.config['player_1_operator'],
                color=self.config['player_1_color'],
                turn_time=self.config['player_1_seconds_per_turn'],
                turns_left=self.config['player_1_turn_limit'],
            ),
            Player.TWO: PlayerFactory.make_player(
                operator=self.config['player_2_operator'],
                color=self.config['player_2_color'],
                turn_time=self.config['player_2_seconds_per_turn'],
                turns_left=self.config['player_2_turn_limit']
            )
        }

        self.players[Player.ONE].special_init()
        self.players[Player.TWO].special_init()

        self.current_player = (
            Player.ONE if self.players[Player.ONE].color == Color.BLACK.value
            else Player.TWO
        )

        self.next_player = (
            Player.TWO if self.current_player == Player.ONE
            else Player.ONE
        )

        self.game_state = "No Game Started"

    def get_board(self):
        """Returns the board.

        :rtype: dict[int, int]
        """
        return self.board

    def get_top_info(self):
        """Returns the information needed for the top info widget"""
        player_1 = self.players[Player.ONE]
        player_2 = self.players[Player.TWO]
        cur_player = self.players[self.current_player]
        info = {
            'game_state': self.game_state,
            'cur_player': f"{f'Player_1-{player_1.operator}' if self.current_player == Player.ONE else f'Player_2-{player_2.operator}'}-{cur_player.color}",
            'player_1_marble_color': player_1.color,
            'player_1_turns_left': player_1.turns_left if player_1.turns_left is not None else "Unlimited",
            'player_1_score': player_1.score,
            'player_1_time_left': player_1.turn_time_max - player_1.turn_time_taken,
            'player_1_operator': player_1.operator,
            'player_2_marble_color': player_2.color,
            'player_2_turns_left': player_2.turns_left if player_2.turns_left is not None else "Unlimited",
            'player_2_score': player_2.score,
            'player_2_time_left': player_2.turn_time_max - player_2.turn_time_taken,
            'player_2_operator': player_2.operator,
        }

        return info

    def cancel_player_turn_timers(self):
        try:
            self.players[self.current_player].cancel_timer()
        except Exception as e:
            print(e)

        try:
            self.players[self.next_player].cancel_timer()
        except Exception as e:
            print(e)

    def swap_players(self):
        self.current_player, self.next_player = self.next_player, self.current_player
        print()

    def execute_string_input(self, action_string):
        origin_half, destination_half = action_string.split('-')

        origin_coord_strings = [origin_half[(i - 1) * 2:2 * i] for i in
                                range(int(len(origin_half) / 2), 0, -1)]
        destination_coord_strings = [destination_half[(i - 1) * 2:2 * i] for i
                                     in
                                     range(int(len(destination_half) / 2), 0,
                                           -1)]

        for origin_coord_string, destination_coord_string in zip(
                origin_coord_strings, destination_coord_strings):

            origin_column_digit = (ord(origin_coord_string[0].upper()) - 64)
            origin_row_digit = int(origin_coord_string[1])

            if destination_coord_string.upper() == "N0":
                del self.board[origin_column_digit * 10 + origin_row_digit]
                self.players[self.current_player].increment_score()
                continue

            destination_column_digit = (
                        ord(destination_coord_string[0].upper()) - 64)
            destination_row_digit = int(destination_coord_string[1])

            marble_color = self.board[
                origin_column_digit * 10 + origin_row_digit]
            del self.board[origin_column_digit * 10 + origin_row_digit]
            self.board[destination_column_digit * 10 + destination_row_digit] = marble_color

    def handle_start_callback(self):
        """Handles start button."""
        self.display_slave.bottom_bar.start_button.configure(state=tk.DISABLED)
        self.display_slave.bottom_bar.input_action_entry.configure(state=tk.NORMAL)
        self.display_slave.bottom_bar.pause_button.configure(state=tk.NORMAL)
        self.display_slave.bottom_bar.reset_button.configure(state=tk.NORMAL)
        self.display_slave.bottom_bar.undo_last_move_button.configure(state=tk.NORMAL)

        self.game_state = "Playing"

        self.players[self.current_player].start_turn(game=self)
        self.players[self.current_player].start_turn_timer()

        self.display_slave.top_info.update_labels()

    def handle_input_confirm_callback(self, user_input):
        """Handles action input confirm event."""

        pre_move_board = self.board.copy()

        self.execute_string_input(
            action_string=user_input,
        )

        self.display_slave.board.update_board()

        cur_player = self.players[self.current_player]

        new_log = LogItem(player=cur_player,
                          move=user_input,
                          original_board=pre_move_board,
                          result_board=self.board.copy(),
                          time_taken=cur_player.turn_time_taken)
        cur_player.log.append(new_log)
        print("\n".join([str(item) for item in cur_player.log]))
        self.display_slave.side_info.update_all()

        cur_player.reset_turn_time_taken()

        cur_player.decrement_turns_left()

        cur_player.cancel_timer()

        self.swap_players()

        new_cur_player = self.players[self.current_player]
        new_cur_player.start_turn_timer()
        new_cur_player.start_turn(game=self)

        self.display_slave.top_info.update_labels()

    def handle_pause_callback(self):
        """Handles pause button."""
        self.cancel_player_turn_timers()

        self.display_slave.bottom_bar.pause_button.configure(state=tk.DISABLED)
        self.display_slave.bottom_bar.resume_button.configure(state=tk.NORMAL)
        self.display_slave.bottom_bar.reset_button.configure(state=tk.NORMAL)


    def handle_resume_callback(self):
        """Handles resume button."""
        self.players[self.current_player].start_turn_timer()

        self.display_slave.bottom_bar.resume_button.configure(state=tk.DISABLED)
        self.display_slave.bottom_bar.pause_button.configure(state=tk.NORMAL)

    def handle_undo_last_move_callback(self):
        """Handles undo last move button."""
        cur_player = self.players[self.current_player]
        prev_player = self.players[self.next_player]

        cur_player.handle_undo()
        prev_player.handle_undo()

        cur_player.reset_turn_time_taken()
        cur_player.cancel_timer()

        prev_log = prev_player.log.pop()

        self.board = prev_log.original_board

        self.swap_players()
        new_cur_player = self.players[self.current_player]
        new_cur_player.increment_turns_left()
        new_cur_player.start_turn_timer()
        new_cur_player.start_turn(game=self)

        self.display_slave.side_info.update_all()
        self.display_slave.board.update_board()
        self.display_slave.top_info.update_labels()

    def handle_reset_callback(self):
        """Handles reset button."""
        print("reset")

    def handle_stop_callback(self):
        """Handles stop button."""
        self.cancel_player_turn_timers()
        self.back_to_config_callback(config=self.config)


    def bind_display(self, display_state):
        self.display_slave = display_state
        self.players[Player.ONE].bind_top_info_callback(self.display_slave.top_info.update_labels)
        self.players[Player.TWO].bind_top_info_callback(self.display_slave.top_info.update_labels)
