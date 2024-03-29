"""Justin's Heuristic function.

eval_attributes:
    defensive:
        weight:
            (int) weight applied to all defensive attributes
        method_list:
            defensive_method_1
            defensive_method_2
            defensive_method_3

    offensive:
        weight:
            (int) weight applied to all offensive attributes
        method_list:
            offensive_method_1, weight
            offensive_method_2, weight
            offensive_method_3, weight

"""
global position_scores

position_scores = {
    95: 0, 96: 0, 97: 0, 98: 0, 99: 0,
    84: 0, 85: 2, 86: 2, 87: 2, 88: 2, 89: 0,
    73: 0, 74: 2, 75: 3, 76: 3, 77: 3, 78: 2, 79: 0,
    62: 0, 63: 2, 64: 3, 65: 4, 66: 4, 67: 3, 68: 2, 69: 0,
    51: 0, 52: 2, 53: 3, 54: 4, 55: 5, 56: 4, 57: 3, 58: 2, 59: 0,
    41: 0, 42: 2, 43: 3, 44: 4, 45: 4, 46: 3, 47: 2, 48: 0,
    31: 0, 32: 2, 33: 3, 34: 3, 35: 3, 36: 2, 37: 0,
    21: 0, 22: 2, 23: 2, 24: 2, 25: 2, 26: 0,
    11: 0, 12: 0, 13: 0, 14: 0, 15: 1
}

# def center_control(ply_board, max_player, *args, **kwargs):
#     """Evaluates the degree of control a player has over the center"""
#     score = 5
#
#     player_marbles = [pm for pm in ply_board.items() if pm[1] == max_player]
#     num_player_marbles = len(player_marbles)
#     for player_marble in player_marbles:
#         player_row = player_marble[0] // 10
#         player_column = player_marble[0] % 10
#         diagonal_manhattan_distance = max(abs(5 - player_row), abs(5 - player_column)) / num_player_marbles
#         score -= diagonal_manhattan_distance
#
#     enemy_marbles = [pm for pm in ply_board.items() if pm[1] == 1 - max_player]
#     num_enemy_marbles = len(enemy_marbles)
#     for enemy_marble in enemy_marbles:
#         enemy_row = enemy_marble[0] // 10
#         enemy_column = enemy_marble[0] % 10
#         diagonal_manhattan_distance = max(abs(5 - enemy_row), abs(5 - enemy_column)) / num_enemy_marbles
#         score += diagonal_manhattan_distance

def center_control(ply_board, max_player, *args, **kwargs):
    """Evaluates the degree of control a player has over the center"""
    score = 0
    num_marbles = len(ply_board)
    for coord, color in ply_board.items():
        if color == max_player:
            # consider dividing by number of player's own marble count
            # if dividing by total marble count, when opponent losees a marble,
            # your centrality score increases
            score += position_scores[coord] / num_marbles
        else:
            score -= position_scores[coord] / num_marbles

    return score

def living_marbles(ply_board, max_player, *args, **kwargs):
    """number of living marbles."""
    score = 0
    num_marbles = len(ply_board)
    for coord, color in ply_board.items():
        if color == max_player:
            score += 1 / num_marbles
        else:
            score -= 2 / num_marbles
    return score


eval_components = (
    (
        1,
        (
            (1, center_control),
            (3, living_marbles)
        )
    ),
    (
        1,
        (

        )
    )
)

def eval_state(*args, **kwargs):

    score = 0
    for category in eval_components:
        for method in category[1]:
            score += category[0] * method[0] * method[1](**kwargs)

    return score



