"""Contains functions for formatting submissions.

Some processes like converting our representation to the class' representation
is specific to the assignment and not necessarily AI. The generation also needs
 to interact with the UI via some interface. Functions that handle those
 pieces of functionality are put here.
"""


def in_to_marbles(in_path: str) -> tuple[dict[int, int], int]:
    """Converts the input file into a dictionary of marbles and player turn.

    The input format is described in the project outline documentation
    and this function converts it into our desired board representation
    as described in this module's docstring under "board dictionary format"
    """
    with open(in_path, 'r') as f:
        player_turn = 0 if 'b' in f.readline() else 1

        board = {}
        for coord in f.readline().split(','):
            column_digit = (ord(coord[0]) - 64)
            row_digit = int(coord[1])
            color = 0 if coord[2] == 'b' else 1
            board[column_digit*10 + row_digit] = color

    return board, player_turn
