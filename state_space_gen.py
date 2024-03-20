"""This module contains functions to generate state space.

This module is taking a more procedural approach since we
won't be keeping any state. Just inputs and outputs for the most part. At most
there might be a simple data class or two.

to save compute resources, things we would have formally put as objects,
will instead be kept primitive. For example, the board state will have a
standard representation, however it will not be formalized as an object.
To aid in understanding and development in this file, definitions will
be put in this docstring

Informal Definition, and Conventions:

    BOARD DICTIONARY FORMAT:
        a dictionary representation of the board, with each marble
        being a coordinate plus colour formatted like so:
            {<column_letter as digit><row_digit> : <0(black) | 1(white)>}

        example:
            ["C5b, C6b, C7w"]
            ->
            {35:0, 36:0, 37:1}

        working with strings is a lot slower than working with ints
        so the string notation will be converted into ints like so:

            column_letter: a..i -> 1..9
            row_digit: remains 1..9
            color: 0 for black, 1 for white


    DELTAS AND DIRECTIONS:
        a delta is the positional change associated with a direction:
            <row_change_digit><column_change_digit>:<direction_string>

        example:
            11:"NE" means "row add 1, column add 1 : is North-East"

                 10:NW     11:NE
                     \     /
                      ⟋  ⟍
            -01:W --  ⎸  ⎹  -- 01:E
                      ⟍  ⟋
                     /     \
                -11:SW    -10:SE


    GROUP:
        a combination of 1, 2, or 3 marbles formatted like so:
            ((<marble_coord>:<marble_color>, ...), delta)

        examples:
            (34, 33, 37)
            (23,)
            (21, 32)


    GROUPMOVE:
        a groupmove is a group of marbles moving in a certain direction
        with the following format:
            ((marble1, ...), delta)

        example:


    GENALL VS DERIVE:
        genall, short for 'generate all', generates all of something,
        derive generates one or a subset of something

        example:
            genall_groupmove generates all groupmoves
            derive_groupmove generates one or a small subset of groupmoves
"""
from pprint import pprint
import utils


def genall_movegroup_resultboard(in_path: str,
                                 moves_path: str,
                                 boardstates_path: str) -> None:
    """Generates files for moves and board states given an input file."""
    board, player_turn = in_to_marbles(in_path)
    print("board: ")
    pprint(board)
    print(f"player_turn: {player_turn}")
    utils.print_board(board)


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


def filter_for_color(board: dict[int, int], color: int):
    """In place, filters the board out for the colors we are looking for."""
    return dict(filter(lambda x: x.value == color, board))


if __name__ == "__main__":
    in_base = "data/in/"
    out_base = "data/out/"
    genall_movegroup_resultboard(in_base+"Test2.input",
                                 out_base+"test1.out.moves",
                                 out_base+"test1.out.board")

    genall_movegroup_resultboard(in_base+"Test1.input",
                                 out_base+"test1.out.moves",
                                 out_base+"test1.out.board")
