"""Contains a heuristic that returns random values."""

def calculate_control(ply_board, max_player):
    max_count = 0
    min_count = 0
    for pos, col in ply_board.items():
        # cam's code, thanks cam!
        match pos:
            case 55:
                distance = 0
            case 65 | 66 | 54 | 56 | 44 | 45:
                distance = 1
            case 75 | 76 | 77 | 67 | 57 | 46 | 35 | 34 | 33 | 43 | 53 | 64:
                distance = 2
            case 85 | 86 | 87 | 88 | 78 | 68 | 58 | 47 | 36 | 25 | 24 | 23 | 22 | 32 | 42 | 52 | 63 | 74 | 85:
                distance = 3
            case 95 | 96 | 97 | 98 | 99 | 89 | 79 | 69 | 59 | 48 | 37 | 26 | 15 | 14 | 13 | 12 | 11 | 21 | 31 | 41 | 51 | 62 | 73 | 84:
                distance = 4
            case _:
                raise ValueError(
                    f"Value {pos} is not valid. Check that all positions on the board are valid.\n{ply_board}")

        if col == max_player:
            max_count += distance
        else:
            min_count += distance

    # returns ratio. the smaller count you have, the closer you are to center. you want the denominator to be smaller.
    return min_count / max_count


def eval_state(ply_board, max_player, *args, **kwargs):
    """Returns a random evaluation result."""
    result = calculate_control(ply_board, max_player)
    return result
