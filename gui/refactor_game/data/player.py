import threading
import tkinter as tk
import abc

from gui.refactor_game.config_page import Operator, Color
from gui.refactor_game.data.log import LogItem
from heuristics import cam_heuristic
from statespace.marblecoords import is_out_of_bounds
from statespace.search import iterative_deepening_alpha_beta_search
from statespace.statespace import apply_move
from statespace.transposition_table_IO import \
    load_transposition_table_from_pickle, load_transposition_table_from_json


class Player(abc.ABC):
    """Represents a player."""
    ONE = 0
    TWO = 1

    def __init__(self, color, operator, turn_time, turns_left):
        self._color = color
        self._operator = operator
        self._turns_left = turns_left
        self._turn_time_max = turn_time
        self._turn_time_taken = 0
        self._score = 0
        self._log = []

        self._turn_timer = None
        self._update_top_info_callback = None

    @abc.abstractmethod
    def special_init(self):
        """Initialization specific to the players called at logical state init"""
        pass

    @abc.abstractmethod
    def start_turn(self, game):
        pass

    def do_timer_tick(self):
        self._turn_timer = threading.Timer(1, self.do_timer_tick)
        self._turn_time_taken += 1
        self._update_top_info_callback()
        self._turn_timer.start()

    def cancel_timer(self):
        try:
            self._turn_timer.cancel()
        except Exception as e:
            print(e)

    def start_turn_timer(self):
        self._turn_timer = threading.Timer(1, self.do_timer_tick)
        self._turn_timer.start()

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

    def start_turn(self, game):
        self.start_turn_timer()
        pass

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
    def __init__(self, turn_time, **kwargs):
        super().__init__(turn_time=float("inf"), **kwargs)
        self._calculation_time_max = turn_time
        self._calculation_time_last_turn = 0
        self._recommendation_history = []
        self.is_first_move = True

    def special_init(self):
        """Initialization specific to the players called at logical state init"""

        # transposition_table_file_name = "./transposition_table.pkl"
        # self._transposition_table = {}
        # try:
        #     self._transposition_table = load_transposition_table_from_pickle(
        #         transposition_table_file_name)
        #     print("loaded transposition_table_from_pickle")
        # except FileNotFoundError:
        #     print("no table found: ./transposition_table.pkl")
        #     self._transposition_table = {}

        transposition_table_file_name = "./transposition_table.json"
        self._transposition_table = load_transposition_table_from_json(
            transposition_table_file_name)

    def start_turn(self, game):
        self.start_turn_timer()
        def after_search_callback(next_move, elapsed_time):
            self.is_first_move = False
            print(next_move, elapsed_time)
            print(self.move_to_action(next_move))

            self._calculation_time_last_turn = elapsed_time

            result_board = game.board.copy()
            apply_move(result_board, groupmove=next_move)

            self._recommendation_history.append(
                LogItem(player=self,
                        move=self.move_to_action(next_move),
                        original_board=game.board.copy(),
                        result_board=result_board,
                        time_taken=elapsed_time)
            )

            game.display_slave.side_info.update_all()

            for log_item in self._recommendation_history:
                print("recommendation_history: ", str(log_item))

        search_thread = threading.Thread(target=self.ai_search_result, kwargs={"game": game, "after_search_callback": after_search_callback})
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
        strategy = cam_heuristic.eval_state


        # need change time to milliseconds?
        input_time_limit = self.turn_time_max
        move, _, elapsed_time = iterative_deepening_alpha_beta_search(game.board, input_player_turn, input_time_limit * 1000,
                                                                      self.turns_left, strategy, self._transposition_table, is_first_move=self.is_first_move)
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
