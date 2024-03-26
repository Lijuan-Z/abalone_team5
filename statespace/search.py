from datetime import datetime
import random

from statespace.statespace import genall_groupmove_resultboard


def iterative_deepening_alpha_beta_search(board, time_limit, player, turns_remaining):
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
    if player == 0:
        return max_value(board, float('-inf'), float('inf'), depth, player, time_limit, turns_remaining)
    else:
        return min_value(board, float('-inf'), float('inf'), depth, player, time_limit, turns_remaining)


def max_value(board, alpha, beta, depth, player, time_limit, turns_remaining):
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
    Applies an evaluation function to the given state,
    returning a numerical result.
    """
    return random.random()  # replace with your evaluation function
