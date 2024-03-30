from statespace.marblecoords import is_out_of_bounds
from statespace.statespace import absolute_directions

# Weights for evaluation metrics: score, center control, marble grouping
WEIGHTS = [1, 2, 1]
MAX_AGGRESSIVENESS = 1.5

# Value associated with each distance from the centre of the board
DISTANCE_PENALTIES = [0, 1, 4, 8, 16]

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

# Max player turns
MAX_PLAYER_TURNS = 80


NORMALIZED_SCORES = {
    # Max player in the lead
    0: 0.0,
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
        total_turns_remaining (int): An estimate of the total turns remaining in the game, used to adjust aggressiveness.
        max_player (int): The player ID (0 or 1) for whom the board is being evaluated.

    Returns: float: An overall score for the board state, with higher values indicating more favorable states for the
    max_player.
    """

    # Basic game info calculations
    player_marbles = {position: player_id for position, player_id in ply_board.items() if player_id == max_player}
    enemy_marbles = {position: player_id for position, player_id in ply_board.items() if player_id == 1 - max_player}
    num_player_marbles = len(player_marbles)
    num_enemy_marbles = len(enemy_marbles)

    # Performance measure calculations

    normalized_score = calculate_normalized_score(num_player_marbles, num_enemy_marbles)
    centre_distance_ratio = calc_centre_ratio(num_player_marbles, num_enemy_marbles, player_marbles, enemy_marbles)

    # marble_groupings = calculate_groupings_for_all_marbles(ply_board, player_marbles, max_player)
    # total_grouping_score, total_danger, total_enemy_disruption = get_marble_grouping_danger_and_disruption(marble_groupings)
    # player_groupings_length = len(genall_groups(ply_board, player_marbles))
    # enemy_groupings_length = len(genall_groups(ply_board, enemy_marbles))
    # marble_groupings_ratio = player_groupings_length / 1 if enemy_groupings_length == 0 else player_groupings_length / enemy_groupings_length

    # normalized_centre_control_ratio = calculate_normalized_centre_control(ply_board, max_player, num_player_marbles,
    #                                                                       num_enemy_marbles)
    # normalized_marble_grouping = calculate_normalized_marble_grouping(total_grouping_score, num_player_marbles)
    # normalized_enemy_disruption = calculate_normalized_enemy_disruption(total_enemy_disruption, num_player_marbles)
    # normalized_marble_danger = calculate_normalized_marble_danger(total_danger, num_player_marbles)
    aggressiveness = calculate_aggressiveness(normalized_score, total_turns_remaining)
    weighted_score = normalized_score * (WEIGHTS[0]) * aggressiveness
    weighted_centre_control = centre_distance_ratio * (WEIGHTS[1])

    # weighted_grouping_ratio = marble_groupings_ratio * (WEIGHTS[2])
    # weighted_marble_grouping = normalized_marble_grouping * (WEIGHTS[2])
    # weighted_enemy_disruption = normalized_enemy_disruption * (WEIGHTS[3])
    # weighted_marble_danger = normalized_marble_danger * (WEIGHTS[4])

    evaluation = weighted_score * aggressiveness + weighted_centre_control - aggressiveness

    # print(evaluation)
    return evaluation

def calculate_normalized_score(num_player_marbles, num_enemy_marbles):
    return NORMALIZED_SCORES[(num_player_marbles, num_enemy_marbles)]


def calc_centre_ratio(num_player_marbles, num_enemy_marbles, player_marbles, enemy_marbles):
    enemy_centre_distance = sum([DISTANCE_PENALTIES_DICT[position] for position in enemy_marbles]) / num_enemy_marbles
    player_centre_distance = sum(
        [DISTANCE_PENALTIES_DICT[position] for position in player_marbles]) / num_player_marbles
    return enemy_centre_distance / player_centre_distance


def calculate_aggressiveness(normalized_score, total_turns_remaining):
    base_aggressiveness = 1 - (total_turns_remaining / MAX_PLAYER_TURNS)  # Increases as the game progresses

    # Adjust base aggressiveness based on whether you're leading or trailing
    if normalized_score > 0:  # Leading
        aggressiveness_adjustment = -normalized_score  # Less aggressive
    else:  # Trailing or even
        aggressiveness_adjustment = abs(normalized_score)  # More aggressive

    # Adjust for game phase
    if total_turns_remaining > (0.7 * MAX_PLAYER_TURNS):
        phase_adjustment = -0.2  # Early game, be more conservative
    elif total_turns_remaining < (0.3 * MAX_PLAYER_TURNS):
        phase_adjustment = 0.2  # Late game, be more aggressive if necessary
    else:
        phase_adjustment = 0  # Mid game, balanced approach

    aggressiveness = base_aggressiveness + aggressiveness_adjustment + phase_adjustment
    return min(max(aggressiveness, 0), MAX_AGGRESSIVENESS)


def genall_groups(board: dict[int, int], player_marbles: dict[int, int]):
    sidestep_groupdirs = []
    for marble in player_marbles.items():
        for direction in absolute_directions:
            new_sidestep_groupdirs = derive_groupdirs(board, marble, direction)
            sidestep_groupdirs.extend(new_sidestep_groupdirs)
    return sidestep_groupdirs


def derive_groupdirs(board: dict[int, int], marble: tuple[int, int], direction: int):
    """Get marble's inline groupmove, sidestep groupdirs, for single direction.

    return format explained:
        output = (inlinegroupmove, list[sidestepgroupdir])
    """
    sidestep_groupdirs = []
    cur_grouping = [marble]
    next_coord = marble[0] + direction
    num_players = 1
    num_enemies = 0

    next_marble = None

    while True:
        try:
            # throws KeyError if no marble at that coordinate
            next_marble = (next_coord, board[next_coord])
        except KeyError:
            next_marble = None
            break
        if is_out_of_bounds(next_coord) \
                or num_players == num_enemies \
                or num_players == 3 and next_marble[1] == marble[1] \
                or next_marble[1] == marble[1] and cur_grouping[-1][1] == 1 - marble[1]:
            break
        cur_grouping.append(next_marble)
        if next_marble[1] == marble[1]:
            sidestep_groupdirs.append((tuple(cur_grouping), direction))
            num_players += 1
        elif next_marble[1] == 1 - marble[1]:
            num_enemies += 1
        next_coord += direction
    return sidestep_groupdirs


def calculate_normalized_marble_grouping(total_grouping_score, num_player_marbles) -> float:
    """
    Normalizes the marble grouping score to assess how well a player's marbles are positioned to support each other.
    Grouping is crucial for both offensive and defensive strategies.

    Parameters:
        total_grouping_score (float): The sum of all 'friendly' neighbor counts for a player's marbles.
        num_player_marbles (int): The number of marbles the player has on the board.

    Returns: float: A normalized score representing the effectiveness of marble grouping, with higher scores
    indicating better grouping.
    """
    max_grouping_score_per_marble = 18.0
    return total_grouping_score / (num_player_marbles * max_grouping_score_per_marble)


def calculate_normalized_enemy_disruption(total_enemy_disruption, num_player_marbles) -> float:
    """
    Evaluates how effectively the player's marbles disrupt the opponent's formations. This metric considers the
    positioning that potentially isolates or splits the opponent's marbles, making them vulnerable or less effective.

    Parameters: total_enemy_disruption (float): The total score based on the player's marbles that are in positions
    to disrupt enemy groupings. num_player_marbles (int): The number of marbles the player has on the board.

    Returns:
        float: A normalized score for disruption, where higher values indicate greater disruption to the opponent.
    """
    max_enemy_disruption_per_marble = 3.0
    return total_enemy_disruption / (num_player_marbles * max_enemy_disruption_per_marble)


def calculate_normalized_marble_danger(total_marble_danger, num_player_marbles) -> float:
    """
    Quantifies the danger to the player's marbles based on their proximity to the board's edges, and
    the number and formation of neighbouring enemy marbles where they risk.

     This metric is crucial for defensive strategies and avoiding losses and scales quickly in Sumito
     situations.

    Parameters:
        total_marble_danger (float): The sum of danger scores for all the player's marbles,
                                     with higher scores indicating closer proximity to edges.
        num_player_marbles (int): The number of marbles the player has on the board.

    Returns:
        float: A normalized danger score, with higher scores indicating greater risk to the player's marbles.
    """
    max_danger_per_marble = 9
    max_total_danger = num_player_marbles * max_danger_per_marble
    return total_marble_danger / 25


def get_neighbors(board, position, player, memo):
    """
    Identifies the neighboring marbles for a given marble position up to three spaces away in each direction,
    categorizing them as either friendlies or enemies. This information is used for calculating marble grouping
    and enemy disruption scores. Results are memoized to avoid redundant calculations.

    Parameters:
        board (dict): The game board representation, mapping positions to player IDs.
        position (int): The current marble's position on the board.
        player (int): The player ID to differentiate friendlies from enemies.
        memo (dict): A dictionary for memoization, caching previously computed neighbor information.

    Returns: dict: A dictionary with directions as keys and sub-dictionaries indicating the counts of friendlies and
    enemies in each direction.
    """
    if (position, player) in memo:
        return memo[(position, player)]
    direction_neighbours = {
        1: {"enemies": 0, "friends": 0},
        10: {"enemies": 0, "friends": 0},
        11: {"enemies": 0, "friends": 0},
        -1: {"enemies": 0, "friends": 0},
        -10: {"enemies": 0, "friends": 0},
        -11: {"enemies": 0, "friends": 0}
    }
    for direction in direction_neighbours:
        temp_position = position + direction
        current_neighbour_color = None
        for _ in range(3):
            if temp_position not in board:
                break
            neighbour = board.get(temp_position)
            if neighbour is not None:
                if current_neighbour_color is None:
                    current_neighbour_color = neighbour
                if neighbour != current_neighbour_color:
                    break
                if neighbour == player:
                    direction_neighbours[direction]["friends"] += 1
                else:
                    direction_neighbours[direction]["enemies"] += 1
            temp_position += direction
    memo[(position, player)] = direction_neighbours
    return memo


def calculate_groupings_for_all_marbles(board, player_marbles, player):
    """
    For all of a player's marbles, calculates the supportive neighbor marbles (groupings) to assess the strength of
    the player's formation. This function aggregates the grouping information for all of a player's marbles, which
    contributes to evaluating the player's defensive positioning and potential for collaborative moves.

    Parameters:
        board (dict): The game board representation, mapping positions to player IDs.
        player_marbles (dict): A dictionary of the player's marbles.
        player (int): The player ID, used to distinguish friendlies from enemies.

    Returns: dict: A memoization dictionary with detailed groupings for each marble, including counts of neighboring
    friendlies and enemies in each direction.
    """
    groupings = {}
    for marble_position in player_marbles:
        groupings = get_neighbors(board, marble_position, player, groupings)
    return groupings


def get_marble_grouping_danger_and_disruption(marble_groupings):
    """
    Analyzes the calculated marble groupings to determine the overall strategic positioning, including the grouping
    strength (support between marbles), the danger to individual marbles (risk of being pushed off), and the level
    of disruption to the opponent's formations. These metrics are crucial for assessing both defensive stability and
    offensive potential.

    Parameters: marble_groupings (dict): Groupings of marbles, with detailed neighbor counts for each marble,
    obtained from calculate_groupings_for_all_marbles.

    Returns: tuple: Contains three float values representing the total grouping score, total marble danger,
    and total enemy disruption score, respectively.
    """
    total_grouping_score = 0.0
    total_danger = 0.0
    total_enemy_disruption = 0.0
    for marble, direction_groupings in marble_groupings.items():
        match marble[0]:
            case 95 | 96 | 97 | 98 | 99 | 89 | 79 | 69 | 59 | 48 | 37 | 26 | 15 | 14 | 13 | 12 | 11 | 21 | 31 | 41 | 51 | 62 | 73 | 84:
                for direction_grouping in direction_groupings.values():
                    total_danger += direction_grouping["enemies"] ** 2
                    total_grouping_score += direction_grouping["friends"]
            case _:
                for direction, neighbours in direction_groupings.items():
                    opposite_direction = -direction
                    total_grouping_score += neighbours["friends"]
                    if opposite_direction in direction_groupings and neighbours["enemies"] > 0 and \
                            direction_groupings[opposite_direction]["enemies"] > 0:
                        total_enemy_disruption += 1
    return total_grouping_score, total_danger, total_enemy_disruption
