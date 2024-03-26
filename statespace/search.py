from datetime import datetime
import random

from statespace.statespace import genall_groupmove_resultboard


def iterative_deepening_alpha_beta_search(board, player, time_limit, turns_remaining):
    """
    Makes calls to alpha_beta_search, incrementing the depth each loop.

    Each call returns the best move for the given player given that depth of search. The function will continue to
    search deeper, unless the time limit is reached.

    Parameters:
        board: a dict representation of the marbles on the board
        time_limit: the total allotted time for this move to be determined. Should be accurate to 1/100ths of a second
        player: a value, 0 or 1, indicating whose turn it is
        turns_remaining: the total remaining turns for the current player

    Returns:
        best_move: the best move found from all iterations the alpha-beta search
    """
    start_time = datetime.now()
    depth = 1
    best_move = None
    while True:
        current_time = datetime.now()
        elapsed_time = (current_time - start_time).total_seconds()
        if elapsed_time >= time_limit:
            break
        temp_move, _ = alpha_beta_search(board, depth, player, time_limit - elapsed_time, turns_remaining)
        if temp_move is not None:
            best_move = temp_move
        depth += 1
    return best_move


def alpha_beta_search(board, depth, player, time_limit, turns_remaining):
    """
    Determines which function should be called as the starting point of the alpha-beta search, based on the
    player value.

    Parameters:
        board: a dict representation of the marbles on the board
        depth: the current depth limit for the search (ie. how many levels deep before the state is evaluated)
        time_limit: the total allotted time for this move to be determined. Should be accurate to 1/100ths of a second
        player: a value, 0 or 1, indicating whose turn it is
        turns_remaining: the total remaining turns for the current player

    Returns:
        (best_move, best_value): A tuple containing the best move for a player and that move's value as determined
        by the evaluation function
    """
    if player == 0:
        return max_value(board, float('-inf'), float('inf'), depth, player, time_limit, turns_remaining)
    else:
        return min_value(board, float('-inf'), float('inf'), depth, player, time_limit, turns_remaining)


def max_value(board, alpha, beta, depth, player, time_limit, turns_remaining):
    """
    Finds and returns the move and value most optimal next move for the Max player given a board state.
    ie. the MAXIMUM VALUE move.

    The purpose of this function is to find the *MAXIMUM value a player can guarantee* given their options

    Parameters:
        board: a dict representation of the marbles on the board
        alpha: a float representing the current best lower bound for the Max player.
        beta: a float representing the current best upper bound for the Min player.
        depth: the current depth limit for the search (ie. how many levels deep before the state is evaluated)
        time_limit: the total allotted time for this move to be determined. Should be accurate to 1/100ths of a second
        player: a value, 0 or 1, indicating whose turn it is
        turns_remaining: the total remaining turns for the current player

    Returns:
        (best_move, best_value): A tuple containing the best move for a player and that move's value as determined
        by the evaluation function
    """
    if game_over(board, turns_remaining, player) or depth == 0:
        return None, evaluate(board, turns_remaining, player)
    best_move = None
    best_value = float('-inf')
    for move, result_board in genall_groupmove_resultboard(board, player):
        _, value = min_value(result_board, alpha, beta, depth - 1, 1 - player, time_limit, turns_remaining - 1)
        if value > best_value:
            best_value = value
            best_move = move
        alpha = max(alpha, value)
        if alpha >= beta:
            break
    return best_move, best_value


def min_value(board, alpha, beta, depth, player, time_limit, turns_remaining):
    """
       Finds and returns the move and value most optimal next move for the Min player given a board state.
       ie. the MINIMUM VALUE move.

       The purpose of this function is to find the *MINIMUM value a player can guarantee* given their options

       Parameters:
           board: a dict representation of the marbles on the board
           alpha: a float representing the current best lower bound for the Max player.
           beta: a float representing the current best upper bound for the Min player.
           depth: the current depth limit for the search (ie. how many levels deep before the state is evaluated)
           player: a value, 0 or 1, indicating whose turn it is
           time_limit: the total allotted time for this move to be determined. Should be accurate to 1/100ths of a second
           turns_remaining: the total remaining turns for the current player

       Returns:
           (best_move, best_value): A tuple containing the best move for the Min player and that move's value as determined
           by the evaluation function
    """

    if game_over(board, turns_remaining, player) or depth == 0:
        return None, evaluate(board, turns_remaining, player)
    best_move = None
    best_value = float('inf')
    for move, result_board in genall_groupmove_resultboard(board, player):
        _, value = max_value(result_board, alpha, beta, depth - 1, 1 - player, time_limit, turns_remaining - 1)
        if value < best_value:
            best_value = value
            best_move = move
        beta = min(beta, value)
        if beta <= alpha:
            break
    return best_move, best_value


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
    return turns_remaining == 0 or num_player_marbles(player, board) == 8


def evaluate(board, turns_remaining, player):
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
    return random.random()  # replace with your evaluation function
