from . import debugutils, external



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
            debugutils.print_board(original_board[0])
            print()
        b = line_to_marbles(line)
        debugutils.print_board(b)
        print("===============================")
        print("===============================")


def print_output_line(line: str):
    print("===============================")
    print("===============================")
    b = line_to_marbles(line)
    debugutils.print_board(b)
    print("===============================")
    print("===============================")


def main():
    import os
    print(os.listdir(os.path.curdir))

    testnum = 1
    print_output_file(f"tests/out/Test{testnum}/Test{testnum}.board")
    print_output_line("I5w,I6w,H4w,H5w,H6w,G4w,G5w,A4w,A5w,B4w,B5w,B6w,C5w,C6w,I8b,I9b,H7b,H8b,H9b,G7b,G8b,A1b,A2b,B1b,B2b,B3b,C2b,C3b")


if __name__ == '__main__':
    main()
