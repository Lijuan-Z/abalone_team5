from heuristics import cam_heuristic
from statespace.search import game_over, num_player_marbles, \
    iterative_deepening_alpha_beta_search
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


def print_board(board, black_marble="🦖", white_marble="🐒", empty_space="🥥"):
    """
    Prints the Abalone board state in a hexagonal pattern based on a given
    board dictionary, correctly displaying with 99 at the top right and 11 at
    the bottom left.
    """

    max_length_row = 9
    for row in rows:
        print("  " * (max_length_row - len(row)), end="")
        for pos in row:
            marble = board.get(pos, empty_space)
            marble_symbol = black_marble if marble == 0 else white_marble if marble == 1 else empty_space
            print(marble_symbol, end=" ")
        print()


def who_won(board):
    """
    Returns the player who won, based on a board state.
    """
    if num_player_marbles(0, board) > num_player_marbles(1, board):
        return "Black Wins!!"
    elif num_player_marbles(0, board) < num_player_marbles(1, board):
        return "White Wins!!"
    else:
        return "It's a tie!!"


def simulate_game(board,
                  transposition_table,
                  total_turns_remaining_per_player=20,
                  time_limit=5000,
                  player_color=0):
    """
      Simulates an Abalone game given the starting conditions.

      Parameters:
      - starting_board: The initial state of the game board.
      - total_turns_remaining_per_player: The total number of turns each player starts with.
      - time_limit: The time limit for each move in milliseconds.
      - player_color: The color of the player who starts the game (0 for Black, 1 for White).
      """
    board = board
    black_player_turns_remaining = total_turns_remaining_per_player
    white_player_turns_remaining = total_turns_remaining_per_player
    player = player_color

    while not game_over(
            board,
            black_player_turns_remaining + white_player_turns_remaining,
            player
    ):
        player_name = "Black" if player == 0 else "White"
        turns_remaining = black_player_turns_remaining \
            if player == 0 else white_player_turns_remaining

        print(f"{player_name} Player's turn.")
        print(f"Turns remaining for {player_name}: {turns_remaining}")
        print(f"Board Positions: {board}\n")
        print_board(board)
        print("\nSearching For Next Move...")
        move, _, _ = iterative_deepening_alpha_beta_search(
            board,
            player,
            time_limit,
            turns_remaining,
            cam_heuristic.eval_state,
            transposition_table,
        )
        print(f"Selected Move: {move}\n")
        apply_move(board, move)

        # Update the remaining turns for the current player
        if player == 0:
            black_player_turns_remaining -= 1
        else:
            white_player_turns_remaining -= 1

        # Switch to the next player
        player = -player + 1
    print(f"{who_won(board)}")


if __name__ == '__main__':
    eval_state = cam_heuristic.eval_state
    turns_remaining = 10
    depth = 5
    transposition_table_filename = (f"{eval_state.__name__}"
                                    f"_turns{turns_remaining}"
                                    f"_depth{depth}.pkl")

    try:
        transposition_table = load_transposition_table_from_pickle(
            transposition_table_filename
        )
    except FileNotFoundError:
        transposition_table = {}

    simulate_game(
        board=starting_boards['standard'],
        transposition_table=transposition_table,
        total_turns_remaining_per_player=turns_remaining,
    )
