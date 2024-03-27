from . import external

def print_board(board: dict):
    board_rep = {11: ' ', 12: ' ', 13: ' ', 14: ' ', 15: ' ', 16: ' ',
                 17: ' ', 18: ' ', 19: ' ', 21: ' ', 22: ' ', 23: ' ',
                 24: ' ', 25: ' ', 26: ' ', 27: ' ', 28: ' ', 29: ' ',
                 31: ' ', 32: ' ', 33: ' ', 34: ' ', 35: ' ', 36: ' ',
                 37: ' ', 38: ' ', 39: ' ', 41: ' ', 42: ' ', 43: ' ',
                 44: ' ', 45: ' ', 46: ' ', 47: ' ', 48: ' ', 49: ' ',
                 51: ' ', 52: ' ', 53: ' ', 54: ' ', 55: ' ', 56: ' ',
                 57: ' ', 58: ' ', 59: ' ', 62: ' ', 63: ' ', 64: ' ',
                 65: ' ', 66: ' ', 67: ' ', 68: ' ', 69: ' ', 73: ' ',
                 74: ' ', 75: ' ', 76: ' ', 77: ' ', 78: ' ', 79: ' ',
                 84: ' ', 85: ' ', 86: ' ', 87: ' ', 88: ' ', 89: ' ',
                 95: ' ', 96: ' ', 97: ' ', 98: ' ', 99: ' '}

    for coord, value in board.items():
        board_rep[coord] = "⚪" if value == 0 else "⬤"

    board_template = f"""        ⟋ ⟍ ⟋ ⟍ ⟋ ⟍ ⟋ ⟍ ⟋ ⟍
        ⎸{board_rep[95]}⎹ ⎸{board_rep[96]}⎹ ⎸{board_rep[97]}⎹ ⎸{board_rep[98]}⎹ ⎸{board_rep[99]}⎹
        ⟍ ⟋ ⟍ ⟋ ⟍ ⟋ ⟍ ⟋ ⟍ ⟋
      ⟋ ⟍ ⟋ ⟍ ⟋ ⟍ ⟋ ⟍ ⟋ ⟍ ⟋ ⟍
      ⎸{board_rep[84]}⎹ ⎸{board_rep[85]}⎹ ⎸{board_rep[86]}⎹ ⎸{board_rep[87]}⎹ ⎸{board_rep[88]}⎹ ⎸{board_rep[89]}⎹
      ⟍ ⟋ ⟍ ⟋ ⟍ ⟋ ⟍ ⟋ ⟍ ⟋ ⟍ ⟋
    ⟋ ⟍ ⟋ ⟍ ⟋ ⟍ ⟋ ⟍ ⟋ ⟍ ⟋ ⟍ ⟋ ⟍
    ⎸{board_rep[73]}⎹ ⎸{board_rep[74]}⎹ ⎸{board_rep[75]}⎹ ⎸{board_rep[76]}⎹ ⎸{board_rep[77]}⎹ ⎸{board_rep[78]}⎹ ⎸{board_rep[79]}⎹
    ⟍ ⟋ ⟍ ⟋ ⟍ ⟋ ⟍ ⟋ ⟍ ⟋ ⟍ ⟋ ⟍ ⟋
  ⟋ ⟍ ⟋ ⟍ ⟋ ⟍ ⟋ ⟍ ⟋ ⟍ ⟋ ⟍ ⟋ ⟍ ⟋ ⟍
  ⎸{board_rep[62]}⎹ ⎸{board_rep[63]}⎹ ⎸{board_rep[64]}⎹ ⎸{board_rep[65]}⎹ ⎸{board_rep[66]}⎹ ⎸{board_rep[67]}⎹ ⎸{board_rep[68]}⎹ ⎸{board_rep[69]}⎹
  ⟍ ⟋ ⟍ ⟋ ⟍ ⟋ ⟍ ⟋ ⟍ ⟋ ⟍ ⟋ ⟍ ⟋ ⟍ ⟋
⟋ ⟍ ⟋ ⟍ ⟋ ⟍ ⟋ ⟍ ⟋ ⟍ ⟋ ⟍ ⟋ ⟍ ⟋ ⟍ ⟋ ⟍
⎸{board_rep[51]}⎹ ⎸{board_rep[52]}⎹ ⎸{board_rep[53]}⎹ ⎸{board_rep[54]}⎹ ⎸{board_rep[55]}⎹ ⎸{board_rep[56]}⎹ ⎸{board_rep[57]}⎹ ⎸{board_rep[58]}⎹ ⎸{board_rep[59]}⎹
⟍ ⟋ ⟍ ⟋ ⟍ ⟋ ⟍ ⟋ ⟍ ⟋ ⟍ ⟋ ⟍ ⟋ ⟍ ⟋ ⟍ ⟋
  ⟋ ⟍ ⟋ ⟍ ⟋ ⟍ ⟋ ⟍ ⟋ ⟍ ⟋ ⟍ ⟋ ⟍ ⟋ ⟍
  ⎸{board_rep[41]}⎹ ⎸{board_rep[42]}⎹ ⎸{board_rep[43]}⎹ ⎸{board_rep[44]}⎹ ⎸{board_rep[45]}⎹ ⎸{board_rep[46]}⎹ ⎸{board_rep[47]}⎹ ⎸{board_rep[48]}⎹
  ⟍ ⟋ ⟍ ⟋ ⟍ ⟋ ⟍ ⟋ ⟍ ⟋ ⟍ ⟋ ⟍ ⟋ ⟍ ⟋
    ⟋ ⟍ ⟋ ⟍ ⟋ ⟍ ⟋ ⟍ ⟋ ⟍ ⟋ ⟍ ⟋ ⟍
    ⎸{board_rep[31]}⎹ ⎸{board_rep[32]}⎹ ⎸{board_rep[33]}⎹ ⎸{board_rep[34]}⎹ ⎸{board_rep[35]}⎹ ⎸{board_rep[36]}⎹ ⎸{board_rep[37]}⎹
    ⟍ ⟋ ⟍ ⟋ ⟍ ⟋ ⟍ ⟋ ⟍ ⟋ ⟍ ⟋ ⟍ ⟋
      ⟋ ⟍ ⟋ ⟍ ⟋ ⟍ ⟋ ⟍ ⟋ ⟍ ⟋ ⟍
      ⎸{board_rep[21]}⎹ ⎸{board_rep[22]}⎹ ⎸{board_rep[23]}⎹ ⎸{board_rep[24]}⎹ ⎸{board_rep[25]}⎹ ⎸{board_rep[26]}⎹
      ⟍ ⟋ ⟍ ⟋ ⟍ ⟋ ⟍ ⟋ ⟍ ⟋ ⟍ ⟋
        ⟋ ⟍ ⟋ ⟍ ⟋ ⟍ ⟋ ⟍ ⟋ ⟍
        ⎸{board_rep[11]}⎹ ⎸{board_rep[12]}⎹ ⎸{board_rep[13]}⎹ ⎸{board_rep[14]}⎹ ⎸{board_rep[15]}⎹
        ⟍ ⟋ ⟍ ⟋ ⟍ ⟋ ⟍ ⟋ ⟍ ⟋        """
    print(board_template)


def print_output_file(filepath: str, original_input_filepath = None):
    with open(filepath, 'r') as f:
        moves = f.readlines()

    with open(filepath, 'r') as f:
        boards = f.readlines()

    for line in boards:
        print("===============================")
        print("===============================")
        if original_input_filepath is not None:
            original_board = external.in_to_marbles("/home/justin/personal/bcit/term3/3981-COMP-intro-to-ai/repos/abalone_team5/data/in/Test1.input")
            print_board(original_board[0])
            print()
        b = external.line_to_marbles(line)
        print_board(b)
        print("===============================")
        print("===============================")


def print_output_line(line: str):
    print("===============================")
    print("===============================")
    b = external.line_to_marbles(line)
    print_board(b)
    print("===============================")
    print("===============================")


if __name__ == "__main__":
    print_board({11: 0, 12: 1})
