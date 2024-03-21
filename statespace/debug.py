import debugutils
import external


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

def print_output_file_line(output_file_line):
    print("===============================")
    print("===============================")
    original_board = external.in_to_marbles("/home/justin/personal/bcit/term3/3981-COMP-intro-to-ai/repos/abalone_team5/data/in/Test1.input")
    debugutils.print_board(original_board[0])
    print()
    b = line_to_marbles(output_file_line)
    debugutils.print_board(b)
    print("===============================")
    print("===============================")





if __name__ == '__main__':
    lines = """c5b,d5b,e4b,e5b,e6b,e7b,f5b,f6b,f8b,g6b,h6b,c3w,c4w,d3w,d4w,d6w,d7w,f4w,f7w,g5w,g7w,g8w,g9w,h8w,h9w
c5b,d5b,e4b,e5b,e6b,f5b,f6b,f7b,f8b,g5b,h6b,c3w,c4w,d3w,d4w,d6w,e7w,f4w,g4w,g6w,g7w,g9w,h7w,h8w,h9w
c5b,d5b,e5b,e6b,f4b,f5b,f6b,f7b,f8b,g6b,h6b,c3w,d3w,d4w,d6w,e4w,e7w,g4w,g5w,g7w,g8w,g9w,h7w,h8w,h9w
c5b,d6b,e4b,e5b,e6b,f5b,f6b,f7b,f8b,g6b,h6b,c3w,c4w,d4w,d5w,d7w,e7w,f4w,g5w,g7w,g8w,g9w,h7w,h8w,h9w"""

    for line in lines.split('\n'):
        print_output_file_line(line)
