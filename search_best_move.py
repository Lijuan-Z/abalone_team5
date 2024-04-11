"""Currently a testing file for the best-move search algorithm."""
from heuristics import cam_heuristic
from statespace.search import game_over, alpha_beta_search_transposition
from statespace.search import \
    iterative_deepening_alpha_beta_search_by_depth as id_abs_bd
from statespace.statespace import apply_move
from statespace.transposition_table_IO import \
    load_transposition_table_from_pickle

starting_boards = {
    'standard': {11: 0, 12: 0, 13: 0, 14: 0, 15: 0, 21: 0, 22: 0,
                 23: 0, 24: 0, 25: 0, 26: 0, 33: 0, 34: 0, 35: 0,
                 99: 1, 98: 1, 97: 1, 96: 1, 95: 1, 89: 1, 88: 1,
                 87: 1, 86: 1, 85: 1, 84: 1, 77: 1, 76: 1, 75: 1},

    'belgian_daisy': {11: 0, 12: 0, 21: 0, 22: 0, 23: 0, 32: 0, 33: 0,
                      99: 0, 98: 0, 89: 0, 88: 0, 87: 0, 78: 0, 77: 0,
                      14: 1, 15: 1, 24: 1, 25: 1, 26: 1, 35: 1, 36: 1,
                      95: 1, 96: 1, 84: 1, 85: 1, 86: 1, 74: 1, 75: 1},

    'german_daisy': {21: 0, 22: 0, 31: 0, 32: 0, 33: 0, 42: 0, 43: 0,
                     67: 0, 68: 0, 77: 0, 78: 0, 79: 0, 88: 0, 89: 0,
                     25: 1, 26: 1, 35: 1, 36: 1, 37: 1, 46: 1, 47: 1,
                     63: 1, 64: 1, 73: 1, 74: 1, 75: 1, 84: 1, 85: 1},

    'sample_1': {35: 0, 45: 0, 54: 0, 55: 0, 56: 0, 65: 0, 66: 0,
                 67: 0, 68: 0, 76: 0, 86: 0, 33: 1, 34: 1, 43: 1,
                 44: 1, 46: 1, 57: 1, 64: 1, 75: 1, 77: 1, 78: 1,
                 79: 1, 87: 1, 88: 1, 89: 1},

    'sample_2': {11: 0, 21: 0, 31: 0, 41: 0, 51: 0, 62: 0, 73: 0,
                 84: 0, 95: 0, 33: 1, 34: 1, 43: 1, 44: 1, 46: 1,
                 57: 1, 64: 1, 75: 1, 77: 1, 78: 1, 79: 1, 87: 1,
                 88: 1, 89: 1}
}


def print_board(board, black_marble="🦖", white_marble="🐒", empty_space="🥥"):
    """
    Prints the Abalone board state in a hexagonal pattern based on a given
    board dictionary, correctly displaying with 99 at the top right and 11 at
    the bottom left.
    """
    rows = [
        [95, 96, 97, 98, 99],
        [84, 85, 86, 87, 88, 89],
        [73, 74, 75, 76, 77, 78, 79],
        [62, 63, 64, 65, 66, 67, 68, 69],
        [51, 52, 53, 54, 55, 56, 57, 58, 59],
        [41, 42, 43, 44, 45, 46, 47, 48],
        [31, 32, 33, 34, 35, 36, 37],
        [21, 22, 23, 24, 25, 26],
        [11, 12, 13, 14, 15]
    ]
    max_length_row = 9
    for row in rows:
        print("  " * (max_length_row - len(row)), end="")
        for pos in row:
            marble = board.get(pos, empty_space)
            marble_symbol = black_marble if marble == 0 else white_marble if marble == 1 else empty_space
            print(marble_symbol, end=" ")
        print()


if __name__ == '__main__':
    board_state = starting_boards["standard"]
    cur_player = 1
    depth = 5
    turns_remaining = [5, 5]
    path = []
    transposition_table = {}

    while not game_over(board_state, turns_remaining[cur_player], cur_player):
        cur_player = 1 - cur_player

        move, path, _ = id_abs_bd(board=board_state,
                         player=cur_player,
                         depth=depth,
                         turns_remaining=turns_remaining[cur_player],
                         eval_callback=cam_heuristic.eval_state,
                         path=path[1:], ab_callback=alpha_beta_search_transposition, transposition_table=transposition_table)

        apply_move(board_state, move)
        print_board(board_state)

        turns_remaining[cur_player] -= 1