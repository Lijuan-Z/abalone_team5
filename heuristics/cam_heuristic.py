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

def get_neighbors(position):
    directions = [-1, -11, -10, 1, 11, 10] # divide these into opposite directions
    return [(position + direction) for direction in directions]

def calculate_marble_grouping_score(board, position, player):
    neighbors = get_neighbors(position)
    grouping_score, surrounding_enemy_score = 0, 0
    for neighbor in neighbors:
        if board.get(neighbor) == player:
            grouping_score += 1
        if board.get(neighbor) == 1-player:
            surrounding_enemy_score += 1
    return grouping_score, surrounding_enemy_score

def calculate_player_grouping_score(board, player_marbles):
    player_score = 0
    disruption_score = 0
    for marble in player_marbles:
        temp_player_score, temp_disruption_score = calculate_marble_grouping_score(board, marble, board[marble])
        player_score += temp_player_score
        disruption_score += temp_disruption_score
    return player_score, disruption_score

def calculate_marble_grouping(board, player):
    return 0

def calculate_normalized_marble_grouping(board, player) -> float:
    marble_grouping = calculate_marble_grouping(board, player)

    return 0


def calculate_normalized_opponent_disruption(board, player) -> float:
    return 0


def calculate_normalized_marble_danger(board, player) -> float:
    return 0


def calculate_aggressiveness_multiplier(normalized_score: float, turns_remaining, player) -> float:
    return 0


def eval_state(ply_board, total_turns_remaining, max_player, *args, **kwargs):
    """
    Evaluates the given board state from the perspective of the specified player.

    Note: This is a placeholder function. You should replace `random.random()` with your actual evaluation logic.

    Parameters:
        ply_board: a dict representation of the marbles on the board.
        total_turns_remaining: the total remaining turns for the current player.
        max_player: a value, 0 or 1, indicating whose perspective to evaluate from.

    Returns:
        float: The evaluated score of the board state for the specified player.
    """

    normalized_score = calculate_normalized_score(ply_board, max_player)
    normalized_centre_control = calculate_normalized_centre_control(ply_board, max_player)
    normalized_marble_grouping = calculate_normalized_marble_grouping(ply_board, max_player)
    normalized_opponent_disruption = calculate_normalized_opponent_disruption(ply_board, max_player)
    normalized_marble_danger = calculate_normalized_marble_danger(ply_board, max_player)
    aggresiveness = calculate_aggressiveness_multiplier(normalized_score, total_turns_remaining, max_player)

    evaluation = (normalized_score * weights[0]
                  + normalized_centre_control * weights[1]
                  + normalized_marble_grouping * weights[2]
                  + normalized_opponent_disruption * weights[3]
                  + normalized_marble_danger * weights[4])
    # print(evaluation, end=", ")
    return evaluation