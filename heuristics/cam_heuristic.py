from statespace.statespace import num_player_marbles


# Weights for evaluation metrics: score, center control, marble grouping, opponent disruption, and marble danger
WEIGHTS = [3, 2, 1, 1, 1]


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

    player_marbles = {position: player_id for position, player_id in ply_board.items() if player_id == max_player}
    num_player_marbles = len(player_marbles)
    marble_groupings = calculate_groupings_for_all_marbles(ply_board, player_marbles, max_player)
    total_grouping_score, total_danger, total_enemy_disruption = get_marble_grouping_danger_and_disruption(
        marble_groupings)

    normalized_score = calculate_normalized_score(ply_board, num_player_marbles)
    normalized_centre_control = calculate_normalized_centre_control(ply_board, max_player)
    normalized_marble_grouping = calculate_normalized_marble_grouping(total_grouping_score, num_player_marbles)
    normalized_enemy_disruption = calculate_normalized_enemy_disruption(total_enemy_disruption, num_player_marbles)
    normalized_marble_danger = calculate_normalized_marble_danger(total_danger, num_player_marbles)
    aggressiveness = calculate_aggressiveness(normalized_score, total_turns_remaining, max_player)
    aggressiveness = 1
    weighted_score = normalized_score * (WEIGHTS[0] + aggressiveness**2)
    weighted_centre_control = normalized_centre_control * (WEIGHTS[1])
    weighted_marble_grouping = normalized_marble_grouping * (WEIGHTS[2] - aggressiveness)
    weighted_enemy_disruption = normalized_enemy_disruption * (WEIGHTS[3] + aggressiveness)
    weighted_marble_danger = normalized_marble_danger * (WEIGHTS[4] - aggressiveness)

    evaluation = weighted_score + weighted_centre_control + weighted_marble_grouping + weighted_enemy_disruption - weighted_marble_danger
    print(evaluation)
    return evaluation


def calculate_normalized_score(board, player_marble_count):
    """
    Calculates the normalized score for a player based on the difference in the number of marbles between the player
    and their opponent. This score reflects the player's progress toward winning the game by pushing off the
    opponent's marbles.

    Parameters:
        board (dict): The game board representation.
        player_marble_count (int): The number of marbles the player has on the board.

    Returns:
        float: A score between -1.0 and 1.0, where higher values indicate a better position for the player.
    """
    return (player_marble_count - (len(board) - player_marble_count)) / 6.0


def calculate_normalized_centre_control(board, player) -> float:
    """
    Calculates how well the player controls the center of the board. It's based on the average Manhattan distance of
    both the player's and the enemy's marbles from the center, normalized to provide a metric indicating control
    dominance.

    Parameters:
        board (dict): The game board representation.
        player (int): The player ID for whom to calculate center control.

    Returns: float: A normalized score indicating the level of control over the center, where higher scores suggest
    stronger control.
    """
    player_avg_distance, enemy_avg_distance = average_distances_from_centre(board, player)
    max_distance = 4
    control_measure = enemy_avg_distance - player_avg_distance
    return enemy_avg_distance / player_avg_distance


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

def calculate_aggressiveness(normalized_score, total_turns_remaining, player) -> float:
    """
    Determines the player's aggressiveness level based on their current score and the estimated turns remaining. This
    metric helps adjust the strategy from defensive to more aggressive as needed to secure a win or mitigate a loss.

    Parameters:
        normalized_score (float): The player's current score, normalized.
        total_turns_remaining (int): An estimate of the total turns remaining in the game.
        player (int): The player ID.

    Returns:
        float: An aggressiveness factor, with higher values indicating a more aggressive strategy.
    """
    turns_remaining_for_player = (total_turns_remaining / 2) + player
    aggression_factor = (1 - turns_remaining_for_player / 400) + abs(normalized_score)
    return min(max(aggression_factor, 0), 2)


def average_distances_from_centre(board, player) -> (float, float):
    """
    Computes the average Manhattan distances from the center of the board for both the player's and the opponent's
    marbles. This metric is used to assess control over the board's central region, which is strategically important
    in Abalone.

    Parameters:
        board (dict): The game board representation, mapping positions to player IDs.
        player (int): The player ID for whom to calculate the average distances.

    Returns:
        tuple of float: A tuple containing two floats:
                         - The first float is the average distance of the player's marbles from the center.
                         - The second float is the average distance of the opponent's marbles from the center.
    """
    player_distance_sum = 0.0
    player_count = 0
    enemy_distance_sum = 0.0
    enemy_count = 0
    for position, color in board.items():
        if color == player:
            count_increment = 1
            distance_sum = player_distance_sum
        else:
            count_increment = 1
            distance_sum = enemy_distance_sum
        match position:
            case 55:
                continue
            case 65 | 66 | 54 | 56 | 44 | 45:
                distance_sum += 1
            case 75 | 76 | 77 | 67 | 57 | 46 | 35 | 34 | 33 | 43 | 53 | 64:
                distance_sum += 2
            case 85 | 86 | 87 | 88 | 78 | 68 | 58 | 47 | 36 | 25 | 24 | 23 | 22 | 32 | 42 | 52 | 63 | 74 | 85:
                distance_sum += 3
            case 95 | 96 | 97 | 98 | 99 | 89 | 79 | 69 | 59 | 48 | 37 | 26 | 15 | 14 | 13 | 12 | 11 | 21 | 31 | 41 | 51 | 62 | 73 | 84:
                distance_sum += 4
            case _:
                raise ValueError(
                    f"Value {position} is not valid. Check that all positions on the board are valid.\n{board}")
        if color == player:
            player_distance_sum = distance_sum
            player_count += count_increment
        else:
            enemy_distance_sum = distance_sum
            enemy_count += count_increment
    player_average_distance = player_distance_sum / player_count if player_count else 0
    enemy_average_distance = enemy_distance_sum / enemy_count if enemy_count else 0
    return player_average_distance, enemy_average_distance


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
