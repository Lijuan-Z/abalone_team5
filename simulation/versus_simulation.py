"""Classes and methods to simulate 2 sets of heuristics competing."""
import time

from .base_simulation import Simulation
from statespace.statespace import iterative_deepening_alpha_beta_search
from statespace.statespace import apply_move


class VersusSimulation(Simulation):
    """Runs a full versus simulation using 2 sets of heuristics."""
    def __init__(self):
        super().__init__()

    def start(self):
        """Starts the simulation"""
        self.board_state = {11: 0, 12: 0, 13: 0, 14: 0, 15: 0, 21: 0, 22: 0, 23: 0, 24: 0, 25: 0, 26: 0, 33: 0, 34: 0, 35: 0, 99: 1, 98: 1, 97: 1, 96: 1, 95: 1, 89: 1, 88: 1, 87: 1, 86: 1, 85: 1, 84: 1, 77: 1, 76: 1, 75: 1}
        player_turn = 0
        self.update_display()


        while True:
            move = iterative_deepening_alpha_beta_search(self.board_state,
                                                         player_turn, 20, 30)
            apply_move(self.board_state, move)
            self.update_display()

            player_turn = 1 - player_turn


        while True:
            self.update_display()
