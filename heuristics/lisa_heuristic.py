def eval_state(init_board, ply_board, max_player, *kwarg, **kwargs):
    max_player_init_pos = [key for key, value in init_board.items() if value == max_player]
    max_player_init_marble_number = len(max_player_init_pos)

    max_player_pos = [key for key, value in ply_board.items() if value == max_player]
    max_player_marble_number = len(max_player_pos)

    opponent_init_pos = [key for key, value in init_board.items() if value == 1 - max_player]
    opponent_init_marble_number = len(opponent_init_pos)

    opponent_pos = [key for key, value in ply_board.items() if value == 1 - max_player]
    opponent_marble_number = len(opponent_pos)
    k1 = -1
    k2 = 1
    k3 = 20
    k4 = -20

    max_player_marble_number_delta = max_player_marble_number - max_player_init_marble_number
    opponent_marble_number_delta = opponent_marble_number - opponent_init_marble_number

    dp = sum(abs((pos // 10) - 5) + abs(pos % 10 - 5) for pos in max_player_pos)
    do = sum(abs((pos // 10) - 5) + abs(pos % 10 - 5) for pos in opponent_pos)
    value = k1 * dp + k2 * do + k3 * max_player_marble_number_delta + k4 * opponent_marble_number_delta

    return value