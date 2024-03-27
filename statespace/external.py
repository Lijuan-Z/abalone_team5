"""Contains functions for formatting submissions.

Some processes like converting our representation to the class' representation
is specific to the assignment and not necessarily AI. The generation also needs
 to interact with the UI via some interface. Functions that handle those
 pieces of functionality are put here.
"""
from . import statespace as ss
from .marblecoords import is_out_of_bounds
import os


def process_folder(folder_path: str) -> None:
    """WRITEME."""
    # Construct the input and output folder paths
    # print("Processing Folder:", folder_path)
    in_folder = os.path.join(folder_path, "in")
    out_folder = os.path.join(folder_path, "out")

    if not os.path.exists(out_folder):
        os.makedirs(out_folder)

    try:
        # print(os.listdir(os.curdir))
        files = os.listdir(in_folder)
    except FileNotFoundError:
        # print("Folder does not exist")
        exit()

    # print("Processing the following files:", files)

    for filename in files:
        basename = ".".join(filename.split(".")[:-1])

        file_out_folder = os.path.join(out_folder, basename)

        if not os.path.exists(file_out_folder):
            os.makedirs(file_out_folder)

        process_file(os.path.join(in_folder, f"{basename}.input"),
                     os.path.join(out_folder, basename, f"{basename}.move"),
                     os.path.join(out_folder, basename, f"{basename}.board"))


def process_file(in_path: str, out_move_path: str, out_board_path: str):
    """WRITEME."""
    board, player_color = in_to_marbles(in_path)
    groupmove_resultboards = ss.genall_groupmove_resultboard(board,
                                                             player_color)

    if os.path.exists(out_move_path):
        os.remove(out_move_path)

    if os.path.exists(out_board_path):
        os.remove(out_board_path)

    with open(out_move_path, "w+") as f_moves:
        with open(out_board_path, "w+") as f_boards:
            for groupmove, resultboard in groupmove_resultboards:
                f_moves.write(move_to_out(groupmove))
                f_boards.write(dict_to_out(resultboard))


def line_to_marbles(line: str) -> dict[int, int]:
    """Converts the input file into a dictionary of marbles and player turn.

    The input format is described in the project outline documentation
    and this function converts it into our desired board representation
    as described in this module's docstring under "board dictionary format"
    """
    board = {}
    for coord in line.split(','):
        coord = coord[0].upper() + coord[1:]
        column_digit = (ord(coord[0]) - 64)
        row_digit = int(coord[1])
        color = 0 if coord[2] == 'b' else 1
        board[column_digit*10 + row_digit] = color

    return board


def in_to_marbles(in_path: str) -> tuple[dict[int, int], int]:
    """Converts the input file into a dictionary of marbles and player turn.

    The input format is described in the project outline documentation
    and this function converts it into our desired board representation
    as described in this module's docstring under "board dictionary format"
    """
    with open(in_path, 'r') as f:
        player_turn = 0 if 'b' in f.readline() else 1
        board = line_to_marbles(f.readline())

    return board, player_turn


def move_to_out(groupmove: tuple[tuple[tuple[int, int], ...], int]) -> str:
    """WRITEME."""
    origin = []
    destination = []

    for marble in groupmove[0]:
        marble_origin_formatted = (chr((marble[0] // 10) + 64)
                                   + str(marble[0] % 10))
        origin.append(marble_origin_formatted)

        marble_destination_formatted = None
        if is_out_of_bounds(marble[0] + groupmove[1]):
            marble_destination_formatted = "N0"
        else:
            marble_destination_formatted = (chr(((marble[0] + groupmove[1]) // 10) + 64)
                                            + str((marble[0] + groupmove[1]) % 10))

        destination.append(marble_destination_formatted)

    return f'{"".join(origin)}-{"".join(destination)}\n'


def dict_to_out(board):
    """WRITEME."""
    out_str = ""

    board_items = board.items()
    blacks = list(filter(lambda item: item[1] == 0, board_items))
    whites = list(filter(lambda item: item[1] == 1, board_items))
    blacks.sort()
    whites.sort()

    all_marbles = blacks + whites
    for coord, color in all_marbles:
        out_str += f"{chr((coord // 10) + 64)}{coord % 10}{'b' if color == 0 else 'w'},"

    return f"{out_str[:-1]}\n"


if __name__ == "__main__":
    process_folder("../tests")
