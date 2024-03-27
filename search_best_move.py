"""Currently a testing file for the best-move search algorithm."""
from statespace import *
from statespace import external, debugutils
from statespace.statespace import iterative_deepening_alpha_beta_search, game_over, apply_move, num_player_marbles


def print_board(board, black_marble="🦖", white_marble="🐒", empty_space="🥥"):
    """
    Prints the Abalone board state in a hexagonal pattern based on a given board dictionary,
    correctly displaying with 99 at the top right and 11 at the bottom left.
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


starting_board = {
    99: 0, 98: 0, 97: 0, 96: 0, 95: 0,
    89: 0, 88: 0, 87: 0, 86: 0, 85: 0, 84: 0,
    75: 0, 76: 0, 77: 0,

    11: 1, 12: 1, 13: 1, 14: 1, 15: 1,
    21: 1, 22: 1, 23: 1, 24: 1, 25: 1, 26: 1,
    35: 1, 34: 1, 33: 1,
}


def who_won(board):
    if num_player_marbles(0, board) > num_player_marbles(1, board):
        return "Black Wins!!"
    elif num_player_marbles(0, board) < num_player_marbles(1, board):
        return "White Wins!!"
    else:
        return "It's a tie!!"


def simulate_game(board, total_turns_remaining_per_player=20, time_limit=5000, player_color=0):
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

    while not game_over(board, black_player_turns_remaining + white_player_turns_remaining, player):
        player_name = "Black" if player == 0 else "White"
        turns_remaining = black_player_turns_remaining if player == 0 else white_player_turns_remaining

        print(f"{player_name} Player's turn.")
        print(f"Turns remaining for {player_name}: {turns_remaining}")
        print(f"Board Positions: {board}\n")
        print_board(board)
        print("\nSearching For Next Move...")
        move = iterative_deepening_alpha_beta_search(board, player, time_limit, turns_remaining, False)
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
    in_base = "tests/statespace_gen_validation/in/"
    out_base = "tests/statespace_gen_validation/out/"

    test_num = 2
    _, player = external.in_to_marbles(f"{in_base}Test{test_num}.input")

    simulate_game(starting_board, 15, 4000, 0)
