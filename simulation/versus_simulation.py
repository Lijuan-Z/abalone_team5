"""Classes and methods to simulate 2 sets of heuristics competing."""
import time

from .base_simulation import Simulation
from statespace.search import iterative_deepening_alpha_beta_search as idab
from statespace.statespace import apply_move
from statespace.search import game_over
from heuristics import random, lisa_heuristic, cam_heuristic, kate_heuristic, \
    justin_heuristic

strategy = {0: justin_heuristic.eval_state, 1: cam_heuristic.eval_state}


class VersusSimulation(Simulation):
    """Runs a full versus simulation using 2 sets of heuristics."""

    def __init__(self, board_config_key = 0):
        super().__init__()

        self.starting_boards = {
            # default
            0: {11: 0, 12: 0, 13: 0, 14: 0, 15: 0, 21: 0, 22: 0,
                23: 0, 24: 0, 25: 0, 26: 0, 33: 0, 34: 0, 35: 0,
                99: 1, 98: 1, 97: 1, 96: 1, 95: 1, 89: 1, 88: 1,
                87: 1, 86: 1, 85: 1, 84: 1, 77: 1, 76: 1, 75: 1},

            # belgian daisy
            1: {11: 0, 12: 0, 21: 0, 22: 0, 23: 0, 32: 0, 33: 0,
                99: 0, 98: 0, 89: 0, 88: 0, 87: 0, 78: 0, 77: 0,
                14: 1, 15: 1, 24: 1, 25: 1, 26: 1, 35: 1, 36: 1,
                95: 1, 96: 1, 84: 1, 85: 1, 86: 1, 74: 1, 75: 1},

            # german daisy
            2: {21: 0, 22: 0, 31: 0, 32: 0, 33: 0, 42: 0, 43: 0,
                67: 0, 68: 0, 77: 0, 78: 0, 79: 0, 88: 0, 89: 0,
                25: 1, 26: 1, 35: 1, 36: 1, 37: 1, 46: 1, 47: 1,
                63: 1, 64: 1, 73: 1, 74: 1, 75: 1, 84: 1, 85: 1},
        }
        self.board_state = self.starting_boards[board_config_key]

    def start(self):
        """Starts the simulation"""
        player_turn = 1  # init as opposite
        turns_remaining = {0: 40, 1: 40}
        time_limit = 300
        # time_limit = 30
        self.update_display()

        while not game_over(self.board_state,
                            turns_remaining[player_turn],
                            player_turn):
            player_turn = 1 - player_turn
            move = idab(self.board_state,
                        player_turn, time_limit,
                        turns_remaining[player_turn],
                        strategy[player_turn])

            if move is None:
                break

            apply_move(self.board_state, move)

            black_marbles_remaining = sum(
                1 for marble in self.board_state.values() if marble == 0)
            white_marbles_remaining = sum(
                1 for marble in self.board_state.values() if marble == 1)
            print(f"Total Remaining Marbles:"
                  f"\tBlack: {black_marbles_remaining}"
                  f"\tWhite: {white_marbles_remaining}")

            self.update_display()
            turns_remaining[player_turn] -= 1

        black_marbles_remaining = sum(
            1 for marble in self.board_state.values() if marble == 0)
        white_marbles_remaining = sum(
            1 for marble in self.board_state.values() if marble == 1)
        winner = "Black" if black_marbles_remaining > white_marbles_remaining else "White"
        print(f"{winner} wins!!!")
        print(f"Total Remaining Marbles:"
              f"\tBlack: {black_marbles_remaining}"
              f"\tWhite: {white_marbles_remaining}")
        while True:
            self.update_display()
