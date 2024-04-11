from statespace.marblecoords import is_out_of_bounds
from statespace.statespace import absolute_directions

# Weights for evaluation metrics: score, center control, marble grouping, enemy disruption, and marble danger
WEIGHTS = [4, 1]

# Value associated with each distance from the centre of the board
DISTANCE_PENALTIES = [0, 2, 4, 6, 10]

# Dict associating board positions with penalty values
DISTANCE_PENALTIES_DICT = {
    55: 0,
    # First ring
    65: DISTANCE_PENALTIES[1],
    66: DISTANCE_PENALTIES[1],
    54: DISTANCE_PENALTIES[1],
    56: DISTANCE_PENALTIES[1],
    44: DISTANCE_PENALTIES[1],
    45: DISTANCE_PENALTIES[1],
    # Second ring
    75: DISTANCE_PENALTIES[2],
    76: DISTANCE_PENALTIES[2],
    77: DISTANCE_PENALTIES[2],
    67: DISTANCE_PENALTIES[2],
    57: DISTANCE_PENALTIES[2],
    46: DISTANCE_PENALTIES[2],
    35: DISTANCE_PENALTIES[2],
    34: DISTANCE_PENALTIES[2],
    33: DISTANCE_PENALTIES[2],
    43: DISTANCE_PENALTIES[2],
    53: DISTANCE_PENALTIES[2],
    64: DISTANCE_PENALTIES[2],
    # Third Ring
    85: DISTANCE_PENALTIES[3],
    86: DISTANCE_PENALTIES[3],
    87: DISTANCE_PENALTIES[3],
    88: DISTANCE_PENALTIES[3],
    78: DISTANCE_PENALTIES[3],
    68: DISTANCE_PENALTIES[3],
    58: DISTANCE_PENALTIES[3],
    47: DISTANCE_PENALTIES[3],
    36: DISTANCE_PENALTIES[3],
    25: DISTANCE_PENALTIES[3],
    24: DISTANCE_PENALTIES[3],
    23: DISTANCE_PENALTIES[3],
    22: DISTANCE_PENALTIES[3],
    32: DISTANCE_PENALTIES[3],
    42: DISTANCE_PENALTIES[3],
    52: DISTANCE_PENALTIES[3],
    63: DISTANCE_PENALTIES[3],
    74: DISTANCE_PENALTIES[3],
    # Fourth ring
    95: DISTANCE_PENALTIES[4],
    96: DISTANCE_PENALTIES[4],
    97: DISTANCE_PENALTIES[4],
    98: DISTANCE_PENALTIES[4],
    99: DISTANCE_PENALTIES[4],
    89: DISTANCE_PENALTIES[4],
    79: DISTANCE_PENALTIES[4],
    69: DISTANCE_PENALTIES[4],
    59: DISTANCE_PENALTIES[4],
    48: DISTANCE_PENALTIES[4],
    37: DISTANCE_PENALTIES[4],
    26: DISTANCE_PENALTIES[4],
    15: DISTANCE_PENALTIES[4],
    14: DISTANCE_PENALTIES[4],
    13: DISTANCE_PENALTIES[4],
    12: DISTANCE_PENALTIES[4],
    11: DISTANCE_PENALTIES[4],
    21: DISTANCE_PENALTIES[4],
    31: DISTANCE_PENALTIES[4],
    41: DISTANCE_PENALTIES[4],
    51: DISTANCE_PENALTIES[4],
    62: DISTANCE_PENALTIES[4],
    73: DISTANCE_PENALTIES[4],
    84: DISTANCE_PENALTIES[4]
}

# Precomputed Normalized Scores
NORMALIZED_SCORES = {
    # Tie (eww)
    0: 0.0,

    # Max player in the lead
    1: 0.167,
    2: 0.333,
    3: 0.5,
    4: 0.667,
    5: 0.833,
    6: 1.0,

    # Min player in the lead
    -1: -0.167,
    -2: -0.333,
    -3: -0.5,
    -4: -0.667,
    -5: -0.833,
    -6: -1.0
}


def eval_state(ply_board, total_turns_remaining, max_player, *args, **kwargs):
    """
    Main function to evaluate the current state of the Abalone game board from the perspective of one player. It
    combines several metrics including score normalization, center control, marble grouping, opponent disruption,
    and marble danger, each adjusted for aggressiveness based on the game state.

    Parameters:
        ply_board (dict): A dictionary representation of the game board with positions as keys and player IDs as values.
        max_player (int): The player ID (0 or 1) for whom the board is being evaluated.

    Returns: float: An overall score for the board state, with higher values indicating more favorable states for the
    max_player.
    """

    # Basic game info calculations
    player_marbles = {position: player_id for position, player_id in ply_board.items() if player_id == max_player}
    enemy_marbles = {position: player_id for position, player_id in ply_board.items() if player_id != max_player}
    num_player_marbles = len(player_marbles)
    num_enemy_marbles = len(enemy_marbles)

    # Performance measure determination
    normalized_score = calculate_normalized_score(num_player_marbles, num_enemy_marbles)
    centre_distance_ratio = calc_centre_ratio(player_marbles, enemy_marbles)

    return normalized_score * (WEIGHTS[0]) + centre_distance_ratio * (WEIGHTS[1])


def calculate_normalized_score(num_player_marbles, num_enemy_marbles):
    return NORMALIZED_SCORES[(num_player_marbles - num_enemy_marbles)]


def calc_centre_ratio(player_marbles, enemy_marbles):
    enemy_centre_distance = sum([DISTANCE_PENALTIES_DICT[position] for position in enemy_marbles])
    player_centre_distance = sum(
        [DISTANCE_PENALTIES_DICT[position] for position in player_marbles])
    return (enemy_centre_distance / player_centre_distance) / 4
