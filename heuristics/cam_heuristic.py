"""
Set weights for score, centre control, marble grouping, opponent disruption, and marble danger respectively
instantiating this outside of the function scope so it's only created once
"""
from statespace.statespace import num_player_marbles

weights = [1, 1, 1, 1, 1]


def calculate_normalized_score(board, player) -> float:
    player_marble_count = num_player_marbles(player, board)
    # print((player_marble_count - (len(board) - player_marble_count)) / 8)
    return (player_marble_count - (len(board) - player_marble_count)) / 8


def average_distances_from_centre(board, player) -> (float, float):
    """
    Returns the average Manhattan distance from the center of the board where a player's and enemy's marbles are.
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


def calculate_normalized_centre_control(board, player) -> float:
    player_avg_distance, enemy_avg_distance = average_distances_from_centre(board, player)
    max_distance = 4

    control_measure = enemy_avg_distance - player_avg_distance

    normalized_centre_control = control_measure / max_distance

    return normalized_centre_control


def calculate_normalized_marble_grouping(board, player) -> float:
    return 0


def calculate_normalized_opponent_disruption(board, player) -> float:
    return 0





def calculate_total_marble_danger(board, position, player):
    total_marble_danger = 0
    for marble in board:
        if not board.get(marble) == player: continue
        match position:
            # dangerous positions (outside ring of board)
            case 95 | 96 | 97 | 98 | 99 | 89 | 79 | 69 | 59 | 48 | 37 | 26 | 15 | 14 | 13 | 12 | 11 | 21 | 31 | 41 | 51 | 62 | 73 | 84:
                total_marble_danger += marble_danger(position)
            case _:
                continue
    return total_marble_danger


def calculate_normalized_marble_danger(board, player) -> float:
    return 0
    # danger = 95 | 96 | 97 | 98 | 99 | 89 | 79 | 69 | 59 | 48 | 37 | 26 | 15 | 14 | 13 | 12 | 11 | 21 | 31 | 41 | 51 | 62 | 73 | 84:
    # return 0


def calculate_aggressiveness_multiplier(normalized_score: float, turns_remaining, player) -> float:
    return 0


def get_neighbors(board, position, player, memo):
    # Check if result is already memoized
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
            else:
                break

            temp_position += direction

    # Store the result in memo before returning
    memo[(position, player)] = direction_neighbours
    return memo


def calculate_groupings_for_all_marbles(board, player_marbles, player):
    memo = {}  # Initialize memoization dictionary
    for marble_position in player_marbles:
        memo = get_neighbors(board, marble_position, player, memo)
    return memo


def calculate_grouping_score(marble_groupings):
    score = 0
    for direction, neighbours in marble_groupings:
        score += neighbours["friends"]
    return score


def marble_danger(marble_groupings):
    total_danger = 0
    for position, direction_groupings in marble_groupings:
        match position:
            case 95 | 96 | 97 | 98 | 99 | 89 | 79 | 69 | 59 | 48 | 37 | 26 | 15 | 14 | 13 | 12 | 11 | 21 | 31 | 41 | 51 | 62 | 73 | 84:
                for direction_grouping in direction_groupings:
                    total_danger += direction_grouping["enemies"]




def eval_state(board, turns_remaining, player):
    """
    Evaluates the given board state from the perspective of the specified player.

    Note: This is a placeholder function. You should replace `random.random()` with your actual evaluation logic.

    Parameters:
        board: a dict representation of the marbles on the board.
        turns_remaining: the total remaining turns for the current player.
        player: a value, 0 or 1, indicating whose perspective to evaluate from.

    Returns:
        float: The evaluated score of the board state for the specified player.
    """
    player_marbles = {position: player_id for position, player_id in board.items() if player_id == player}
    # marble_groupings = calculate_groupings_for_all_marbles(board, player_marbles, player)
    # marble_grouping_score = calculate_grouping_score(marble_groupings.values())
    #
    # print(marble_groupings)
    normalized_score = calculate_normalized_score(board, player)
    normalized_centre_control = calculate_normalized_centre_control(board, player)
    normalized_marble_grouping = calculate_normalized_marble_grouping(board, player)
    normalized_opponent_disruption = calculate_normalized_opponent_disruption(board, player)
    normalized_marble_danger = calculate_normalized_marble_danger(board, player)
    aggresiveness = calculate_aggressiveness_multiplier(normalized_score, turns_remaining, player)
    evaluation = (normalized_score * weights[0]
                  + normalized_centre_control * weights[1]
                  + normalized_marble_grouping * weights[2]
                  + normalized_opponent_disruption * weights[3]
                  + normalized_marble_danger * weights[4])
    # print(evaluation, end=", ")
    return evaluation
