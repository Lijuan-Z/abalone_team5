"""Contains a heuristic that returns random values."""

distance_mapping = {
    55: 0,
    65: 1, 66: 1, 54: 1, 56: 1, 44: 1, 45: 1,
    75: 2, 76: 2, 77: 2, 67: 2, 57: 2, 46: 2, 35: 2, 34: 2, 33: 2, 43: 2, 53: 2, 64: 2,
    85: 3, 86: 3, 87: 3, 88: 3, 78: 3, 68: 3, 58: 3, 47: 3, 36: 3, 25: 3, 24: 3, 23: 3, 22: 3, 32: 3, 42: 3, 52: 3, 63: 3, 74: 3,
    95: 10, 96: 10, 97: 10, 98: 10, 99: 10, 89: 10, 79: 10, 69: 10, 59: 10, 48: 10, 37: 10, 26: 10, 15: 10, 14: 10, 13: 10, 12: 10, 11: 10, 21: 10, 31: 10, 41: 10, 51: 10, 62: 10, 73: 10, 84: 10
}
directions = [1, 10, 11]


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
    # print("max, min", (max, min))
    return max - min


def density(ply_board, max_player):
    num = 0
    den = 0
    danger_count = [0, 0]

    for marble in ply_board.items():
        for direction in directions:
            if marble[0] + direction in ply_board.keys():
                num += 1 - max_player
                if distance_mapping[marble[0]] == 10 and marble[0] + direction in ply_board.keys() and ply_board[marble[0] + direction] == 1 - marble[1] and ply_board[marble[0] + direction] == 1 - marble[1]:
                    danger_count[marble[1]] += 1
            if marble[0] - direction in ply_board.keys():
                num += 1 - max_player
                if distance_mapping[marble[0]] == 10 and marble[0] - direction in ply_board.keys() and ply_board[marble[0] - direction] == 1 - marble[1] and ply_board[marble[0] - direction] == 1 - marble[1]:
                    danger_count[marble[1]] += 1

            den += 1 - max_player

    # print("num den", (num/den, num/den))
    # print("danger_count", (danger_count[max_player], danger_count[1 - max_player]))
    # print()
    return (num / den) + (2 * (danger_count[1 - max_player] - danger_count[max_player]))


def eval_state(ply_board, total_turns_remaining, max_player, *args, **kwargs):
    """Returns a random evaluation result."""
    heuristics = {
        middle_control: total_turns_remaining * 0.02,
        marble_loss: 20,
        density: 0.6,
    }

    sum = 0
    for heuristic, weight in heuristics.items():
        result = heuristic(ply_board, max_player)
        print(heuristic.__name__, result * weight)
        sum += result * weight
    # print()
    return sum
