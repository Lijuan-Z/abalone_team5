from . import debugutils, external


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

def print_output_file(filepath: str):
    with open(filepath, 'r') as f:
        moves = f.readlines()

    with open(filepath, 'r') as f:
        boards = f.readlines()

    for line in boards:
        print("===============================")
        print("===============================")
        original_board = external.in_to_marbles("/home/justin/personal/bcit/term3/3981-COMP-intro-to-ai/repos/abalone_team5/data/in/Test1.input")
        debugutils.print_board(original_board[0])
        print()
        b = line_to_marbles(line)
        debugutils.print_board(b)
        print("===============================")
        print("===============================")


if __name__ == '__main__':
    import os
    print(os.listdir(os.path.curdir))

    testnum = 1
    print_output_file(f"../tests/out/Test{testnum}/Test{testnum}.board")
