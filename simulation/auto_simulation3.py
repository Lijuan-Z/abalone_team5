import copy
import os
from datetime import datetime

from random import randint
from statespace.search import iterative_deepening_alpha_beta_search as idab
from statespace.statespace import apply_move
from statespace.search import game_over
from heuristics import random, lisa_heuristic, cam_heuristic, kate_heuristic, \
    justin_heuristic, agg_heuristic
import pandas as pd

from statespace.transposition_table_IO import load_transposition_table_from_pickle


def generate_writable_excel_path(base_path):
    index = 1  # Start with an index for file naming
    while True:
        try:
            # Check if the file exists to avoid unnecessary opening attempts
            if os.path.exists(base_path):
                # Attempt to open the file in append mode just to check writability
                with open(base_path, 'a'):
                    pass
                break
            else:
                break
        except (IOError, PermissionError):
            base_name, extension = os.path.splitext(base_path)
            base_path = f"{base_name}_{index}{extension}"
            index += 1
    return base_path


file_list = [cam_heuristic, kate_heuristic]
starting_boards = {
    # standard
    0: {11: 0, 12: 0, 13: 0, 14: 0, 15: 0, 21: 0, 22: 0,
        23: 0, 24: 0, 25: 0, 26: 0, 33: 0, 34: 0, 35: 0,
        99: 1, 98: 1, 97: 1, 96: 1, 95: 1, 89: 1, 88: 1,
        87: 1, 86: 1, 85: 1, 84: 1, 77: 1, 76: 1, 75: 1},

    # belgian daisy
    1: {11: 0, 12: 0, 21: 0, 22: 0, 23: 0, 32: 0, 33: 0,
        99: 0, 98: 0, 89: 0, 88: 0, 87: 0, 78: 0, 77: 0,
        14: 1, 15: 1, 24: 1, 25: 1, 26: 1, 35: 1, 36: 1,
        95: 1, 96: 1, 84: 1, 85: 1, 86: 1, 74: 1, 75: 1},

    # germain daisy
    2: {21: 0, 22: 0, 31: 0, 32: 0, 33: 0, 42: 0, 43: 0,
        67: 0, 68: 0, 77: 0, 78: 0, 79: 0, 88: 0, 89: 0,
        25: 1, 26: 1, 35: 1, 36: 1, 37: 1, 46: 1, 47: 1,
        63: 1, 64: 1, 73: 1, 74: 1, 75: 1, 84: 1, 85: 1}
}
start_time = datetime.now()
turn_limits = [30]
time_limits = [5000]
winners_name = ""
wins_counter = {}
for heuristic in file_list:
    player_name = heuristic.__name__.split('.')[1].split('_')[0]
    wins_counter[player_name] = 0
records = []
for board_config_key in [0, 1, 2]:
    layout = {0: "standard", 1: "belgian daisy", 2: "german daisy"}.get(board_config_key, "")
    for turn_limit in turn_limits:
        for time_limit in time_limits:
            for evaluation_black in file_list:
                for evaluation_white in file_list:
                    if evaluation_white != evaluation_black:
                        board_state = copy.deepcopy(starting_boards[board_config_key])
                        player_turn = 1  # Black starts
                        turns_remaining = {0: turn_limit, 1: turn_limit}
                        strategy = {0: evaluation_black.eval_state, 1: evaluation_white.eval_state}
                        winner = ""
                        first_move = None
                        first_turn = True

                        black_author_name = evaluation_black.__name__.split('.')[1].split('_')[0]
                        white_author_name = evaluation_white.__name__.split('.')[1].split('_')[0]
                        print(f"Simulating {black_author_name} vs. {white_author_name}, {layout}")
                        transposition_table_file_names = [f"transposition_table_{black_author_name}.pkl",
                                                          f"transposition_table_{white_author_name}.pkl"]
                        transposition_tables = [{}, {}]
                        try:
                            # transposition_tables[0] = load_transposition_table_from_pickle(
                            #     transposition_table_file_names[0])
                            transposition_tables[0] = {}
                        except FileNotFoundError:
                            transposition_tables[0] = {}
                        try:
                            # transposition_tables[1] = load_transposition_table_from_pickle(
                            #     transposition_table_file_names[1])
                            transposition_tables[1] = {}
                        except FileNotFoundError:
                            transposition_tables[1] = {}

                        # Simulation loop
                        while not game_over(board_state, turns_remaining[player_turn], player_turn):
                            player_turn = 1 - player_turn
                            if first_turn:
                                first_move = idab(board_state,
                                                                           player_turn,
                                                                           time_limit,
                                                                           turns_remaining[player_turn],
                                                                           transposition_table=transposition_tables[
                                                                               player_turn],
                                                                           eval_callback=strategy[player_turn],
                                                                           is_first_move=first_turn,
                                                                           t_table_filename=
                                                                           transposition_table_file_names[player_turn])
                                apply_move(board_state, first_move)
                                first_turn = False
                                continue

                            move, transposition_tables[player_turn] = idab(board_state,
                                                                           player_turn,
                                                                           time_limit,
                                                                           turns_remaining[player_turn],
                                                                           transposition_table=transposition_tables[
                                                                               player_turn],
                                                                           eval_callback=strategy[player_turn],
                                                                           is_first_move=first_turn,
                                                                           t_table_filename=
                                                                           transposition_table_file_names[player_turn])
                            if move is None:
                                break
                            apply_move(board_state, move)
                            turns_remaining[player_turn] -= 1

                        black_marbles_remaining = sum(value == 0 for value in board_state.values())
                        white_marbles_remaining = sum(value == 1 for value in board_state.values())

                        if black_marbles_remaining > white_marbles_remaining:
                            winner = "Black"
                            winners_name = black_author_name
                        elif black_marbles_remaining < white_marbles_remaining:
                            winner = "White"
                            winners_name = white_author_name
                        else:
                            winner = "Tie"
                            winners_name = "N/A"

                        if winner != "Tie":
                            wins_counter[winners_name] = wins_counter.get(winners_name, 0) + 1
                        results = {
                            "Black Player": black_author_name,
                            "White Player": white_author_name,
                            "Starting Board Layout": layout,
                            "First Move": first_move,
                            "Time Limit Per Move (ms)": time_limit,
                            "Turn Limit Per Player": turn_limit,
                            "Black Marbles Remaining": black_marbles_remaining,
                            "White Marbles Remaining": white_marbles_remaining,
                            "Winner Color": winner,
                            "Winner Name": winners_name,
                        }
                        for player_name in wins_counter.keys():
                            results[player_name] = wins_counter.get(player_name, 0)
                        records.append(results)
                        print(results)
                        
records.append(wins_counter)

df = pd.DataFrame(records)

base_excel_path = "game_results3.xlsx"
excel_path = generate_writable_excel_path(base_excel_path)
print(f"Printing results to {excel_path}")
with pd.ExcelWriter(excel_path, engine='xlsxwriter') as writer:
    df.to_excel(writer, sheet_name='Game Results', index=False)
print(datetime.now() - start_time)