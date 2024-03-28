def eval_state(init_board, ply_board, max_player,total_turns_remaining):

    max_player_init_pos = [key for key, value in init_board.items() if value == max_player]

    max_player_init_marble_number = len(max_player_init_pos)
    max_player_center_init_pos = sum(max_player_init_pos) / max_player_init_marble_number
    max_player_init_distance = sum(pos - max_player_center_init_pos for pos in max_player_init_pos)

    max_player_pos = [key for key, value in ply_board.items() if value == max_player]
    max_player_marble_number = len(max_player_pos)
    center_pos = sum(max_player_pos) / max_player_marble_number
    max_player_distance = sum(pos - center_pos for pos in max_player_pos)

    opponent_init_pos = [key for key, value in init_board.items() if value == 1 - max_player]
    opponent_init_marble_number = len(opponent_init_pos)
    opponent_center_init_pos = sum(opponent_init_pos) / opponent_init_marble_number
    opponent_init_distance = sum(pos - opponent_center_init_pos for pos in opponent_init_pos)

    opponent_pos = [key for key, value in ply_board.items() if value == 1 - max_player]
    opponent_marble_number = len(opponent_pos)
    opponent_center_pos = sum(opponent_pos) / opponent_marble_number
    opponent_distance = sum(pos - opponent_center_pos for pos in opponent_pos)
    k1 = -2
    k2 = 1
    k3 = 20
    k4 = -10
    max_player_distance_delta = max_player_distance - max_player_init_distance
    opponent_distance_delta = opponent_distance - opponent_init_distance
    max_player_marble_number_delta = max_player_marble_number - max_player_init_marble_number
    opponent_marble_number_delta = opponent_marble_number - opponent_init_marble_number
    value = (k1 * max_player_distance_delta + k2 * opponent_distance_delta +
             k3 * max_player_marble_number_delta + k4 * opponent_marble_number_delta)

    return value