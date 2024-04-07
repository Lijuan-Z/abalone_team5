from datetime import datetime

from statespace.statespace import genall_groupmove_resultboard, apply_move


def iterative_deepening_alpha_beta_search(board, player, time_limit, turns_remaining, eval_callback):
    """
    Makes calls to alpha_beta_search, incrementing the depth each loop.

    Each call returns the best move for the given player given that depth of search. The function will continue to
    search deeper, unless the time limit is reached.

    Parameters:
        board: a dict representation of the marbles on the board
        time_limit: the total allotted time for this move to be determined in milliseconds. Should be accurate to 1/100ths of a second
        player: a value, 0 or 1, indicating whose turn it is
        turns_remaining: the total remaining turns for the current player

    Returns:
        best_move: the best move found from all iterations the alpha-beta search
    """

    start_time = datetime.now()
    depth = 1
    # The total remaining turns in the game will be equal to double one player's remaining turns,
    # and for white the total will be -1 because they always go after black.
    total_turns_remaining = turns_remaining * 2 - player
    best_move = None
    elapsed_time = 0
    best_move_search_time = 0
    time_limit_seconds = time_limit / 1000.0  # Convert time_limit to seconds for comparison

    # The loop will end before the time limit if the maximum depth (based on turns remaining) is reached.

    while depth <= total_turns_remaining:
        temp_move, _ = alpha_beta_search(board, board, float('-inf'), float('inf'), depth, player, player, time_limit_seconds - elapsed_time, total_turns_remaining, eval_callback, )
        elapsed_time = (datetime.now() - start_time).total_seconds()
        if elapsed_time >= time_limit_seconds:
            break
        if temp_move is not None:
            best_move = temp_move
            best_move_search_time = elapsed_time
            depth += 1
    print("\n=======FINISHED========")
    print(f"Best Move Search Time: {best_move_search_time * 1000:.2f}ms/{time_limit:.2f}ms")  # Display in milliseconds
    print(f"Best Move Depth: {depth}")
    print(f"Best Move: {best_move}")

    return best_move


def iterative_deepening_alpha_beta_search_by_depth(board, player, depth, turns_remaining, eval_callback, path):
    start_time = datetime.now()
    cur_depth = 1
    cur_path = path
    best_move = None

    while cur_depth <= depth and cur_depth <= turns_remaining:
        best_move, best_index, _ = alpha_beta_search(board, board, float('-inf'), float('inf'), cur_depth, cur_depth, player, player, 0, turns_remaining, eval_callback, cur_path)
        elapsed_time = (datetime.now() - start_time).total_seconds()
        if cur_path[0] != best_index:
            cur_path = [best_index]
        print("\n=======PLY FINISHED========")
        print(f"Search Time: {elapsed_time * 1000:.2f}ms")  # Display in milliseconds
        print(f"Depth: {cur_depth}")
        print(f"Best Move: {best_move}")
        print(f"Path: {cur_path}")
        cur_depth += 1

    return best_move, cur_path


def alpha_beta_search(init_board, ply_board, alpha, beta, total_depth, depth, max_player, cur_ply_player, time_limit, total_turns_remaining, eval_callback, path):
    """
    Determines which function should be called as the starting point of the alpha-beta search, based on the
    player value.

    Parameters:
        board: a dict representation of the marbles on the board
        depth: the current depth limit for the search (ie. how many levels deep before the state is evaluated)
        time_limit: the total allotted time for this move to be determined. Should be accurate to 1/100ths of a second
        max_player: a value, 0(black) or 1(white), indicating whose turn it is in the game
        cur_ply_player: a value, 0(black) or 1(white), indicating whose turn it is in the current ply
        turns_remaining: the total remaining turns for the current player

    Returns:
        (best_move, best_move_index, best_value): A tuple containing the best move for a player, move index, and that move's value as determined
        by the evaluation function
    """
    if depth == 0 or total_turns_remaining == 0 or num_player_marbles(cur_ply_player, ply_board) == 8:
        return None, None, eval_callback(init_board=init_board, ply_board=ply_board,
                                         total_turns_remaining=total_turns_remaining, max_player=max_player,
                                         time_limit=time_limit)

    best_move = None
    best_move_index = None
    best_gm_rb = None
    continue_search = True
    groupmove_resultboard = genall_groupmove_resultboard(ply_board, cur_ply_player)
    try:
        best_gm_rb = groupmove_resultboard[path[total_depth - depth]]
    except Exception:
        try:
            path[total_depth - depth]
        except Exception:
            path.append(None)

    if cur_ply_player == max_player:
        best_value = float('-inf')
        if best_gm_rb:
            _, _, value = alpha_beta_search(init_board, best_gm_rb[1], alpha, beta, total_depth, depth - 1, max_player, 1 - cur_ply_player, time_limit, total_turns_remaining - 1, eval_callback, path)
            if value > best_value:
                best_value = value
                best_move = best_gm_rb[0]
                best_move_index = path[total_depth - depth]
            if value >= beta:
                continue_search = False
            if value > alpha:
                alpha = value
        if continue_search is True:
            for i, (move, result_board) in enumerate(groupmove_resultboard):
                _, _, value = alpha_beta_search(init_board,result_board, alpha, beta, total_depth, depth - 1, max_player, 1 - cur_ply_player, time_limit, total_turns_remaining - 1, eval_callback, path)
                if value > best_value:
                    best_value = value
                    best_move = move
                    best_move_index = i
                if value >= beta:
                    break
                if value > alpha:
                    alpha = value
    else:
        best_value = float('inf')
        if best_gm_rb:
            _, _, value = alpha_beta_search(init_board, best_gm_rb[1], alpha, beta, total_depth, depth - 1, max_player, 1 - cur_ply_player, time_limit, total_turns_remaining - 1, eval_callback, path)
            if value < best_value:
                best_value = value
                best_move = best_gm_rb[0]
                best_move_index = path[total_depth - depth]
            if value <= alpha:
                continue_search = True
            if value < beta:
                beta = value
        if continue_search is True:
            for i, (move, result_board) in enumerate(groupmove_resultboard):
                _, _, value = alpha_beta_search(init_board,result_board, alpha, beta, total_depth, depth - 1, max_player, 1 - cur_ply_player, time_limit, total_turns_remaining - 1, eval_callback, path)
                if value < best_value:
                    best_value = value
                    best_move = move
                    best_move_index = i
                if value <= alpha:
                    break
                if value < beta:
                    beta = value

    if path[total_depth - depth] is None:
        path[total_depth - depth] = best_move_index
    return best_move, best_move_index, best_value

def num_player_marbles(player, board):
    """
       Counts the number of marbles belonging to a given player on the board.

       Parameters:
           player: a value, 0 or 1, indicating the player whose marbles to count.
           board: a dict representation of the marbles on the board.

       Returns:
           int: The number of marbles belonging to the specified player.
    """
    return sum(1 for value in board.values() if value == player)


def game_over(board, turns_remaining, player):
    """
    Evaluates if the current board state is a 'game_over'

    :param: state, an object representing the positions of marbles and time remaining
    :return: A bool result
    """
    return turns_remaining == 0 or sum(1 for value in board.values() if value == player) == 8