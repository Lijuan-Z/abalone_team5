import threading
import tkinter as tk
import abc

from gui.refactor_game.config_page import Operator


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


class AIPlayer(Player):
    def __init__(self, turn_time, **kwargs):
        super().__init__(turn_time=float("inf"), **kwargs)
        self._calculation_time_max = turn_time
        self._calculation_time_last_turn = 0

    @property
    def turn_time_max(self) -> int or None:
        """Returns the time per turn."""
        return self._calculation_time_max

    @property
    def turn_time_taken(self) -> int or None:
        """Returns the time per turn."""
        return self._calculation_time_last_turn


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
