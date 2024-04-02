import copy
import os
from datetime import datetime
from itertools import product
from multiprocessing import Process, Manager

from logger import create_logger
from statespace.search import iterative_deepening_alpha_beta_search as idab
from statespace.statespace import apply_move
from statespace.search import game_over
from heuristics import lisa_heuristic, cam_heuristic, kate_heuristic, \
    justin_heuristic
import pandas as pd

heuristic_list = [cam_heuristic, justin_heuristic, kate_heuristic, lisa_heuristic]
turn_limits = [50]
time_limits = [100]
board_layouts = ["standard", "belgian_daisy", "german_daisy"]

class AutoSim(Process):
    starting_boards = {
        # standard
        "standard": {11: 0, 12: 0, 13: 0, 14: 0, 15: 0, 21: 0, 22: 0,
                     23: 0, 24: 0, 25: 0, 26: 0, 33: 0, 34: 0, 35: 0,
                     99: 1, 98: 1, 97: 1, 96: 1, 95: 1, 89: 1, 88: 1,
                     87: 1, 86: 1, 85: 1, 84: 1, 77: 1, 76: 1, 75: 1},

        # belgian daisy
        "belgian_daisy": {11: 0, 12: 0, 21: 0, 22: 0, 23: 0, 32: 0, 33: 0,
                          99: 0, 98: 0, 89: 0, 88: 0, 87: 0, 78: 0, 77: 0,
                          14: 1, 15: 1, 24: 1, 25: 1, 26: 1, 35: 1, 36: 1,
                          95: 1, 96: 1, 84: 1, 85: 1, 86: 1, 74: 1, 75: 1},

        # german daisy
        "german_daisy": {21: 0, 22: 0, 31: 0, 32: 0, 33: 0, 42: 0, 43: 0,
                         67: 0, 68: 0, 77: 0, 78: 0, 79: 0, 88: 0, 89: 0,
                         25: 1, 26: 1, 35: 1, 36: 1, 37: 1, 46: 1, 47: 1,
                         63: 1, 64: 1, 73: 1, 74: 1, 75: 1, 84: 1, 85: 1}
    }

    def __init__(self, turn_limit_per_player: int, time_limit_per_move: int, board_layout: str, black_player_heuristic,
                 white_player_heuristic, wins_counter, results_list):
        super().__init__()
        self.board_state = copy.deepcopy(self.starting_boards[board_layout])
        self.turn_limit_per_player = turn_limit_per_player
        self.turns_remaining = {0: turn_limit_per_player, 1: turn_limit_per_player}
        self.time_limit_per_move = time_limit_per_move
        self.board_layout = board_layout
        self.transposition_tables = [{}, {}]
        self.first_move = None

        self.black_player_heuristic = black_player_heuristic.eval_state
        self.black_player_name = black_player_heuristic.__name__.split('.')[1].split('_')[0]
        self.black_marbles_remaining = 14

        self.white_player_heuristic = white_player_heuristic.eval_state
        self.white_player_name = white_player_heuristic.__name__.split('.')[1].split('_')[0]
        self.white_marbles_remaining = 14

        self.winner_colour = ""
        self.winner = "N/A"

        self.wins_counter = wins_counter
        self.results_list = results_list

    def run(self):
        start_time = datetime.now()
        print(f"Simulating {self.black_player_name} vs. {self.white_player_name}, {self.board_layout}")
        logger = create_logger(f"{self.black_player_name}_vs_{self.white_player_name}_{self.board_layout}_{self.turn_limit_per_player}_turns_{self.time_limit_per_move}ms.log")
        player_turn = 1  # Black starts
        while not game_over(self.board_state, self.turns_remaining[player_turn], player_turn):
            player_turn = 1 - player_turn
            if self.first_move is None:
                self.first_move = idab(self.board_state,
                                       player_turn,
                                       self.time_limit_per_move,
                                       self.turns_remaining[player_turn],
                                       transposition_table=self.transposition_tables[player_turn],
                                       logger=logger,
                                       eval_callback=self.black_player_heuristic if player_turn == 0 else self.white_player_heuristic,
                                       is_first_move=True,
                                       t_table_filename=
                                       f"transposition_table_{self.black_player_name}.pkl" if player_turn == 0 else f"transposition_table_{self.white_player_name}.pkl")
                apply_move(self.board_state, self.first_move)
                continue

            move, self.transposition_tables[player_turn] = idab(self.board_state,
                                                                player_turn,
                                                                self.time_limit_per_move,
                                                                self.turns_remaining[player_turn],
                                                                transposition_table=self.transposition_tables[
                                                                    player_turn],
                                                                logger=logger,
                                                                eval_callback=self.black_player_heuristic if player_turn == 0 else self.white_player_heuristic,
                                                                is_first_move=False,
                                                                t_table_filename=
                                                                f"transposition_table_{self.black_player_name}.pkl" if player_turn == 0 else f"transposition_table_{self.white_player_name}.pkl")
            if move is None:
                break

            apply_move(self.board_state, move)
            self.turns_remaining[player_turn] -= 1
        self.black_marbles_remaining = sum(value == 0 for value in self.board_state.values())
        self.white_marbles_remaining = sum(value == 1 for value in self.board_state.values())

        if self.black_marbles_remaining > self.white_marbles_remaining:
            self.winner_colour = "Black"
            self.winner = self.black_player_name
        elif self.black_marbles_remaining < self.white_marbles_remaining:
            self.winner_colour = "White"
            self.winner = self.black_player_name
        else:
            self.winner_colour = "Tie"
            self.winner = "N/A"

        if self.winner != "N/A":
            self.wins_counter[self.winner] = self.wins_counter.get(self.winner, 0) + 1
        results = {
            "Black Player": self.black_player_name,
            "White Player": self.white_player_name,
            "Starting Board Layout": self.board_layout,
            "First Move": self.first_move,
            "Time Limit": f"{self.time_limit_per_move}ms",
            "Turn Limit": self.turn_limit_per_player,
            "Black Marbles Remaining": self.black_marbles_remaining,
            "White Marbles Remaining": self.white_marbles_remaining,
            "Winner Color": self.winner_colour,
            "Winner Name": self.winner,
            "Game Duration": f"{(datetime.now() - start_time).total_seconds() *1000:.2f}ms"
        }
        self.results_list.append(results)
        print(f"Finished: {results}")
        logger.info(results)


def run_simulations(simulation_kwargs_list):
    processes = []
    with Manager() as manager:
        wins_counter = manager.dict()
        results_list = manager.list()

        # Start all simulations
        for kwargs in simulation_kwargs_list:
            process = AutoSim(**kwargs, wins_counter=wins_counter, results_list=results_list)
            processes.append(process)
            process.start()

        # Wait for all simulations to finish
        for process in processes:
            process.join()

        # Collect all results
        results = [result for result in results_list]
        return results, dict(wins_counter)


def generate_writable_excel_path(base_path="game_results.xlsx"):
    index = 1
    while True:
        try:
            if not os.path.exists(base_path):
                break
            else:
                with open(base_path, 'a'):
                    pass
                break
        except (IOError, PermissionError):
            base_name, extension = os.path.splitext(base_path)
            base_path = f"{base_name}_{index}{extension}"
            index += 1
    return base_path


def write_results_to_excel(results, filename="game_results.xlsx"):
    df = pd.DataFrame(results)
    excel_path = generate_writable_excel_path(filename)
    with pd.ExcelWriter(excel_path, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Game Results', index=False)
    print(f"Results have been written to {excel_path}")


if __name__ == '__main__':
    # Generate the Cartesian product of all simulation arguments
    # this is such a dope function.
    simulation_args_list = list(product(turn_limits, time_limits, board_layouts, heuristic_list, heuristic_list))

    # Filter out simulations where the black and white heuristics would be the same
    simulation_args_list = [args for args in simulation_args_list if args[3] != args[4]]

    simulation_kwargs_list = [
        {
            'turn_limit_per_player': args[0],
            'time_limit_per_move': args[1],
            'board_layout': args[2],
            'black_player_heuristic': args[3],
            'white_player_heuristic': args[4]
        }
        for args in simulation_args_list
    ]

    # Now call the run_simulations function with this list
    results, wins_counter = run_simulations(simulation_kwargs_list)

    write_results_to_excel(results)
    for key, value in wins_counter.items():
        print(f"{key}: {value} wins")
