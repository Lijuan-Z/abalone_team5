"""Contains a heuristic that returns random values."""

distance_mapping = {
    55: 0,
    65: 1, 66: 1, 54: 1, 56: 1, 44: 1, 45: 1,
    75: 2, 76: 2, 77: 2, 67: 2, 57: 2, 46: 2, 35: 2, 34: 2, 33: 2, 43: 2, 53: 2, 64: 2,
    85: 3, 86: 3, 87: 3, 88: 3, 78: 3, 68: 3, 58: 3, 47: 3, 36: 3, 25: 3, 24: 3, 23: 3, 22: 3, 32: 3, 42: 3, 52: 3, 63: 3, 74: 3,
    95: 4, 96: 4, 97: 4, 98: 4, 99: 4, 89: 4, 79: 4, 69: 4, 59: 4, 48: 4, 37: 4, 26: 4, 15: 4, 14: 4, 13: 4, 12: 4, 11: 4, 21: 4, 31: 4, 41: 4, 51: 4, 62: 4, 73: 4, 84: 4
}

def middle_control(ply_board, max_player):
    max_count = 0
    min_count = 0
    for pos, col in ply_board.items():
        distance = distance_mapping[pos]

        if col == max_player:
            max_count += distance
        else:
            min_count += distance

    # returns ratio. the smaller count you have, the closer you are to center. you want the denominator to be smaller.
    return min_count / max_count


def marble_loss(ply_board, max_player):
    max = sum([1 for col in ply_board.values() if col == max_player])
    min = len(ply_board) - max
    return 14 - min


def eval_state(ply_board, max_player, *args, **kwargs):
    """Returns a random evaluation result."""
    heuristics = {
        middle_control: 1,
        marble_loss: 1,
    }

    sum = 0
    for heuristic, weight in heuristics.items():
        result = heuristic(ply_board, max_player)
        print(heuristic.__name__, result)
        sum += heuristic(ply_board, max_player) * weight
    print()
    return sum
