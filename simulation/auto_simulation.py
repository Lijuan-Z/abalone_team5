import copy

from statespace.search import iterative_deepening_alpha_beta_search as idab
from statespace.statespace import apply_move
from statespace.search import game_over
from heuristics import random, lisa_heuristic, cam_heuristic, kate_heuristic, \
    justin_heuristic

file_list = [cam_heuristic,justin_heuristic,kate_heuristic,lisa_heuristic]
starting_boards = {
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

    # germain daisy
    2: {21: 0, 22: 0, 31: 0, 32: 0, 33: 0, 42: 0, 43: 0,
        67: 0, 68: 0, 77: 0, 78: 0, 79: 0, 88: 0, 89: 0,
        25: 1, 26: 1, 35: 1, 36: 1, 37: 1, 46: 1, 47: 1,
        63: 1, 64: 1, 73: 1, 74: 1, 75: 1, 84: 1, 85: 1}
}
turns_limit = 30
time_limit = 30
# time_limit = 300
records = []
winners_name = []
for board_config_key in [1, 0, 2]:
    layout = "default" if board_config_key == 0 else "belgian daisy"
    for evaluation_black in file_list:
        for evaluation_white in file_list:
            if evaluation_white != evaluation_black:
                # configuration
                board_state = copy.deepcopy(starting_boards[board_config_key])
                player_turn = 1  # init as opposite
                turns_remaining = {0: turns_limit, 1: turns_limit}

                strategy = {0: evaluation_black.eval_state, 1: evaluation_white.eval_state}

                while not game_over(board_state,
                                    turns_remaining[player_turn],
                                    player_turn):
                    player_turn = 1 - player_turn
                    move = idab(board_state,
                                player_turn, time_limit,
                                turns_remaining[player_turn],
                                strategy[player_turn])

                    if move is None:
                        break

                    apply_move(board_state, move)

                    black_marbles_remaining = sum(
                        1 for marble in board_state.values() if marble == 0)
                    white_marbles_remaining = sum(
                        1 for marble in board_state.values() if marble == 1)
                    # print(f"Total Remaining Marbles:"
                    #       f"\tBlack: {black_marbles_remaining}"
                    #       f"\tWhite: {white_marbles_remaining}")

                    turns_remaining[player_turn] -= 1
                black_marbles_remaining = sum(
                    1 for marble in board_state.values() if marble == 0)
                white_marbles_remaining = sum(
                    1 for marble in board_state.values() if marble == 1)
                winner = "Black" if black_marbles_remaining > white_marbles_remaining else "White"

                black_file_name = evaluation_black.__name__
                second_part = black_file_name.split('.')[1]
                black_author_name = second_part.split('_')[0]

                white_file_name = evaluation_white.__name__
                second_part = white_file_name.split('.')[1]
                white_author_name = second_part.split('_')[0]
                winners_name.append(black_author_name if winner=='Black' else white_author_name)
                record = ("layout", layout, "black", black_author_name, "white", white_author_name, "winner", winner,
                          "black marbles remaining", black_marbles_remaining, "white marbles remaining",
                          white_marbles_remaining,
                          "turns_remaining", turns_remaining)
                records.append(record)
count_cam = winners_name.count('cam')
count_justin = winners_name.count('justin')
count_kate = winners_name.count('kate')
count_lisa = winners_name.count('lisa')
with open("output.txt", "w") as f:
    for record in records:
        record_str = ",".join(map(str, record))
        f.write(record_str + "\n")
    f.write(f"=====winner count information=====\n")
    f.write(f"Count of 'cam': {count_cam}\n")
    f.write(f"Count of 'justin': {count_justin}\n")
    f.write(f"Count of 'kate': {count_kate}\n")
    f.write(f"Count of 'lisa': {count_lisa}\n")