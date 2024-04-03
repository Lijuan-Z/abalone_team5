import tkinter as tk

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
