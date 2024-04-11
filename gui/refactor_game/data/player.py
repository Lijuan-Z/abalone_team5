import threading
import tkinter as tk
import abc
from time import sleep

from gui.refactor_game.config_page import Operator, Color
from gui.refactor_game.data.log import LogItem
from heuristics import cam_heuristic
from statespace.marblecoords import is_out_of_bounds
from statespace.search import iterative_deepening_alpha_beta_search
from statespace.statespace import apply_move
from statespace.transposition_table_IO import \
    load_transposition_table_from_pickle, load_transposition_table_from_json, save_transposition_table_to_json


class Player(abc.ABC):
    """Represents a player."""
    ONE = 0
    TWO = 1

    def __init__(self, player_num, color, operator, turn_time, turns_left, **kwargs):
        self.player_num = player_num
        self._color = color
        self._operator = operator
        self._turns_left = turns_left
        self._turn_time_max = turn_time
        self._turn_time_taken = 0
        self._score = 0
        self._log = []

        self._turn_timer = None
        self._turn_timer_stop = True

        self._update_top_info_callback = None

    @abc.abstractmethod
    def special_init(self):
        """Initialization specific to the players called at logical state init"""
        pass

    def start_turn(self, game):
        self._turn_time_taken = 0
        self.start_turn_timer(game)

    def do_timer_tick(self, game):
        if self._turn_timer_stop:
            return
        self._turn_time_taken += 1
        self._update_top_info_callback()
        # game.parent.display_state.top_info.player_time_left_stringvar[self.player_num].set(self.turn_time_max - self.turn_time_taken)
        game.parent.after(10, self.do_timer_tick, game)

    def cancel_timer(self):
        self._turn_timer_stop = True

    def start_turn_timer(self, game):
        self._turn_timer_stop = False
        game.parent.after(10, self.do_timer_tick, game)

    def bind_top_info_callback(self, update_top_info_callback):
        self._update_top_info_callback = update_top_info_callback

    @property
    def color(self):
        return self._color

    @property
    def turns_left(self):
        return self._turns_left

    def increment_turns_left(self):
        self._turns_left += 1

    @property
    def score(self):
        return self._score

    def increment_score(self):
        self._score += 1

    def decrement_score(self):
        self._score -= 1

    @property
    def log(self):
        return self._log

    @property
    def operator(self):
        return self._operator

    def reset_turn_time_taken(self):
        self._turn_time_taken = 0

    def decrement_turns_left(self):
        self._turns_left -= 1

    @property
    @abc.abstractmethod
    def turn_time_max(self) -> int or None:
        """Returns the time per turn."""
        pass

    @property
    @abc.abstractmethod
    def turn_time_taken(self) -> int or None:
        """Returns the time per turn."""
        pass

    @abc.abstractmethod
    def handle_undo(self):
        pass


class HumanPlayer(Player):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def turn_time_max(self) -> int or None:
        """Returns the time per turn."""
        return self._turn_time_max

    @property
    def turn_time_taken(self) -> int or None:
        """Returns the time per turn."""
        return self._turn_time_taken

    def handle_undo(self):
        pass

    def special_init(self):
        """Initialization specific to the players called at logical state init"""
        pass


class AIPlayer(Player):
    def __init__(self, turn_time, backend_conn, **kwargs):
        super().__init__(turn_time=float("inf"), **kwargs)
        self.backend_conn = backend_conn
        self._calculation_time_max = turn_time
        self._calculation_time_last_turn = 0
        self._recommendation_history = []
        self.is_first_move = True

    def special_init(self):
        """Initialization specific to the players called at logical state init"""
        pass

    def start_turn(self, game):
        def after_search_callback(next_move, elapsed_time):
            self.is_first_move = False
            print(next_move, elapsed_time)
            print(self.move_to_action(next_move))

            print('cancelling timer')
            self.cancel_timer()
            self._calculation_time_last_turn = elapsed_time * 100
            self._turn_time_taken = elapsed_time * 100
            self._update_top_info_callback()

            result_board = game.board.copy()
            apply_move(result_board, groupmove=next_move)

            self._recommendation_history.append(
                LogItem(player=self,
                        move=self.move_to_action(next_move),
                        original_board=game.board.copy(),
                        result_board=result_board,
                        time_taken=round(elapsed_time, 2))
            )

            game.display_slave.side_info.update_all()

            for log_item in self._recommendation_history:
                print("recommendation_history: ", str(log_item))

        search_thread = threading.Thread(target=self.ai_search_result,
                                         kwargs={"game": game, "after_search_callback": after_search_callback})
        self.start_turn_timer(game)
        search_thread.start()

    def handle_undo(self):
        self._recommendation_history.pop()
        self._calculation_time_last_turn = 100000
        pass

    @property
    def turn_time_max(self) -> int or None:
        """Returns the time per turn."""
        return self._calculation_time_max

    @property
    def turn_time_taken(self) -> int or None:
        """Returns the time per turn."""
        # return self._calculation_time_last_turn
        return self._turn_time_taken

    def ai_search_result(self, game, after_search_callback):
        input_player_turn = 0 if self.color == Color.BLACK.value else 1

        # need change time to milliseconds?
        input_time_limit = self.turn_time_max

        request = {
            'board': game.board,
            'player': input_player_turn,
            'time_limit': input_time_limit * 10,  # Adjust time unit
            'turns_remaining': self.turns_left,
            'is_first_move': self.is_first_move
        }
        self.backend_conn.send(request)

        move, elapsed_time = self.backend_conn.recv()
        after_search_callback(move, elapsed_time)

    def move_to_action(self, move):
        source_pos, direction = move
        print(source_pos, direction)
        source = ""
        destination = ""
        for pos in source_pos:
            source += (chr((pos[0] // 10) + 96) + str(pos[0] % 10))
            dest = pos[0] + direction
            if not is_out_of_bounds(dest):
                destination += (chr((dest // 10) + 96) + str(dest % 10))
            else:
                destination += "n0"
        action = source + "-" + destination
        return action


class PlayerFactory:
    """builds a player object."""

    @classmethod
    def make_player(cls, operator, **kwargs) -> Player:
        """returns a player"""
        if operator == Operator.HUMAN.value:
            return HumanPlayer(operator=operator, **kwargs)
        if operator == Operator.AI.value:
            return AIPlayer(operator=operator, **kwargs)
        else:
            raise ValueError(f"operator {operator} is not supported")
