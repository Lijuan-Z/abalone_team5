"""This module contains functions to generate state space.

This module is taking a more procedural approach since we
won't be keeping any state. Just inputs and outputs for the most part. At most
there might be a simple data class or two.

to save compute resources, things we would have formally put as objects,
will instead be kept primitive. For example, the board state will have a
standard representation, however it will not be formalized as an object.
To aid in understanding and development in this file, definitions will
be put in this docstring

Informal Definition, and Conventions:

    BOARD DICTIONARY FORMAT:
        a dictionary representation of the board, with each marble
        being a coordinate plus colour formatted like so:
            {<column_letter as digit><row_digit> : <0(black) | 1(white)>}

        example:
            ["C5b, C6b, C7w"]
            ->
            {35:0, 36:0, 37:1}

        working with strings is a lot slower than working with ints
        so the string notation will be converted into ints like so:

            column_letter: a..i -> 1..9
            row_digit: remains 1..9
            color: 0 for black, 1 for white


    DELTAS AND DIRECTIONS:
        a delta is the positional change associated with a direction:
            <row_change_digit><column_change_digit>:<direction_string>

        example:
            11:"NE" means "row add 1, column add 1 : is North-East"

                 10:NW     11:NE
                     \     /
                      ⟋  ⟍
             -1:W --  ⎸  ⎹  -- 1:E
                      ⟍  ⟋
                     /     \
                -11:SW    -10:SE


    GROUP:
        a tuple of 1, 2, or 3 marbles formatted like so:
            ((<marble_coord>,<marble_color>), ...)

        examples:
            ( (34,1), (33,1), (37,1) )
            a group of 3 white marbles

            ( (23,0) )
            a single white marble

            ( (21,0), (32,1) )
            a black and a white marble


    GROUPMOVE:
        a groupmove is a group of marbles moving in a certain direction
        with the following format:
            ((marble, ...), delta)

        example:
        ( ((33,0), (34,0), (35,1)), 1 )
        this is a 2-black, 1-white sumito in the east direction


    GROUPDIR:
        an enriched group with a facing direction.
        **Not to be mistaken for a groupmove**
        this is a type of group that has an attached a direction it is "facing"
        but is not necessarily moving in. it has the following format:
            ((marble, ...), facing_direction)

        example:
        ( ((33,1), (34,1), (35,1)), 1 )
        this tells us this is a group of marbles laying along the -1<-->1 axis
        but not necessarily moving towards that direction


    GENALL VS DERIVE:
        genall, short for 'generate all', generates all of something,
        derive generates one or a subset of something

        example:
            genall_groupmove generates all groupmoves
            derive_groupmove generates one or a small subset of groupmoves
"""
from datetime import datetime
from random import random

# import debugutils
from .marblecoords import is_out_of_bounds

absolute_directions = [10, 11, 1]


def genall_groupmove_resultboard(marbles: dict[int, int],
                                 player_color: int) \
        -> list[tuple[tuple[tuple[tuple[int, int], ...], int], dict[int, int]]]:
    """Generates all groupmoves and the resulting board from those moves.

    return format explained:
        output = list[(groupmove, resultant_board)]

        groupmove = (group, direction)
        resultant_board = dict{marble_coord: marble_color}

        group = (marble, ...)
        direction = int

        marble = {coord : color}

        coord = int
        color = int
    """
    groupmove_resultboards = []
    player_marbles = dict(filter(lambda marble: marble[1] == player_color,
                                 marbles.items()))

    inlinegroupmoves, sidestepgroupmoves = genall_groupmoves(marbles,
                                                             player_marbles)

    for move in inlinegroupmoves:
        resultant_board = marbles.copy()
        apply_move(resultant_board, move)
        groupmove_resultboards.append((move, resultant_board))

    for move in sidestepgroupmoves:
        resultant_board = marbles.copy()
        apply_move(resultant_board, move)
        groupmove_resultboards.append((move, resultant_board))

    return groupmove_resultboards


def genall_groupmoves(board: dict[int, int],
                      player_marbles: dict[int, int]) \
        -> tuple[list[tuple[tuple[tuple[int], ...], int]],
        list[tuple[tuple[tuple[int], ...], int]]]:
    """Generates all groupmoves given a dict of marbles and the current board.

    return format explained:
        list[groupmove]
    """
    inlinegroupmoves, sidestepgroupdirs = \
        genall_inlinegroupmoves_sidestepgroupdirs(board, player_marbles)

    sidestepgroupmoves = derive_sidestepgroupmoves(board, sidestepgroupdirs)
    return inlinegroupmoves, sidestepgroupmoves


def derive_sidestepgroupmoves(board: dict[int, int],
                              sidestep_groupdirs: list[tuple[tuple[tuple[int, int], ...], int]]) \
        -> list[tuple[tuple[tuple[int, int], ...], int]] | list:
    """Get all sidestep moves of a given sidestep groupdir.

    return format explained:
        output = list[groupmove]
    """
    sidestepgroupmoves = []

    for groupdir in sidestep_groupdirs:
        for direction in absolute_directions:
            if direction == groupdir[1]:
                continue

            if is_valid_sidemove(board, groupdir[0], direction):
                sidestepgroupmoves.append((groupdir[0], direction))

            if is_valid_sidemove(board, groupdir[0], -direction):
                sidestepgroupmoves.append((groupdir[0], -direction))

    return sidestepgroupmoves


def is_valid_sidemove(board: dict[int, int],
                      group: tuple[tuple[int, int], ...],
                      direction: int) -> bool:
    """True if groupdir being moved in direction is a valid sidemove."""
    for marble in group:
        new_coord = marble[0] + direction
        try:
            board[new_coord]
            return False
        except KeyError:
            pass

        if is_out_of_bounds(new_coord):
            return False

    return True


def genall_inlinegroupmoves_sidestepgroupdirs(board: dict[int, int],
                                              player_marbles: dict[int, int]) \
        -> tuple[list[tuple[tuple[tuple[int, int], ...], int]],
        list[tuple[tuple[tuple[int, int], ...], int]]]:
    """Generates all inline groupmoves and sidestep groupdirs.

    outputs two lists due to optimization. We can generate these two
    lists in one go, but it does make the code a little more complicated

    return format explained:
        output = (list[inline_groupmove], list[sidestep_groupdirs])

        inline_groupmoves = list[groupmove]
        sidestep_groupdirs = list[groupdirs]
    """
    inline_groupmoves = []
    sidestep_groupdirs = []

    for marble in player_marbles.items():
        for direction in absolute_directions:
            new_inline_groupmoves, new_sidestep_groupdirs = \
                derive_inlinegroupmove_sidestepgroupdirs(board,
                                                         marble,
                                                         direction)
            if new_inline_groupmoves is not None:
                inline_groupmoves.append(new_inline_groupmoves)
            sidestep_groupdirs.extend(new_sidestep_groupdirs)

            new_inline_groupmoves = \
                derive_inlinegroupmove(board,
                                       marble,
                                       -direction)
            if new_inline_groupmoves is not None:
                inline_groupmoves.append(new_inline_groupmoves)

    return inline_groupmoves, sidestep_groupdirs


def derive_inlinegroupmove_sidestepgroupdirs(board: dict[int, int],
                                             marble: tuple[int, int],
                                             direction: int) \
        -> tuple[tuple[tuple[tuple[int, int], ...], int] | None,
        list[tuple[tuple[tuple[int, int], ...], int]]]:
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
        # if next == AVAILABLE: break
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

    if is_out_of_bounds(next_coord) and cur_grouping[-1][1] == marble[1]:
        return None, sidestep_groupdirs
    elif num_players == 3 and next_marble and next_marble[1] == marble[1]:
        return None, sidestep_groupdirs
    elif next_marble and next_marble[1] == marble[1] and cur_grouping[-1][1] == 1 - marble[1]:
        return None, sidestep_groupdirs
    elif num_players > num_enemies:
        return (tuple(cur_grouping), direction), sidestep_groupdirs
    else:
        return None, sidestep_groupdirs


def derive_inlinegroupmove(board: dict[int, int],
                           marble: tuple[int, int],
                           direction: int) \
        -> tuple[tuple[tuple[int, int], ...], int] | None:
    """Get marble's inline groupmove for single direction.

    return format explained:
        output = (inlinegroupmove, list[sidestepgroupdir])
    """
    cur_grouping = [marble]
    next_coord = marble[0] + direction
    num_players = 1
    num_enemies = 0

    next_marble = None

    while True:
        # if next == AVAILABLE: break
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
            num_players += 1
        elif next_marble[1] == 1 - marble[1]:
            num_enemies += 1

        next_coord += direction

    if is_out_of_bounds(next_coord) and cur_grouping[-1][1] == marble[1]:
        return None
    elif num_players == 3 and next_marble and next_marble[1] == marble[1]:
        return None
    elif next_marble and next_marble[1] == marble[1] and cur_grouping[-1][1] == 1 - marble[1]:
        return None
    elif num_players > num_enemies:
        return tuple(cur_grouping), direction
    else:
        return None


def apply_move(board, groupmove):
    """Apply the given move to the given board state."""
    for marble in reversed(groupmove[0]):
        del board[marble[0]]
        new_coord = marble[0] + groupmove[1]
        if is_out_of_bounds(new_coord):
            continue
        board[marble[0] + groupmove[1]] = marble[1]


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
    time_limit_seconds = time_limit / 1000.0  # Convert time_limit to seconds for comparison

    # The loop will end before the time limit if the maximum depth (based on turns remaining) is reached.
    while depth <= total_turns_remaining:
        current_time = datetime.now()
        elapsed_time = (current_time - start_time).total_seconds()
        if elapsed_time >= time_limit_seconds:
            break
        temp_move, _ = alpha_beta_search(board, board, float('-inf'), float('inf'), depth, player, player, time_limit_seconds - elapsed_time, total_turns_remaining, eval_callback)
        if temp_move is not None:
            best_move = temp_move
        depth += 1
        print(f"Elapsed time: {elapsed_time * 1000:.2f}ms/{time_limit:.2f}ms")  # Display in milliseconds
        print(f"Depth Reached: {depth}")
        print(f"Current Best Move: {best_move}")
    print("\n=======FINISHED========")
    print(f"Elapsed time: {elapsed_time * 1000:.2f}ms/{time_limit:.2f}ms")  # Display in milliseconds
    print(f"Depth Reached: {depth}")
    print(f"Current Best Move: {best_move}")

    return best_move


def alpha_beta_search(init_board, ply_board, alpha, beta, depth, max_player, cur_ply_player, time_limit, total_turns_remaining, eval_callback):
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
        (best_move, best_value): A tuple containing the best move for a player and that move's value as determined
        by the evaluation function
    """
    if game_over(ply_board, total_turns_remaining, cur_ply_player) or depth == 0:
        return None, eval_callback(init_board=init_board, ply_board=ply_board,
                                   total_turns_remaining=total_turns_remaining, max_player=max_player)
    if cur_ply_player == max_player:
        best_move = None
        best_value = float('-inf')
        for move, result_board in genall_groupmove_resultboard(ply_board, cur_ply_player):
            _, value = alpha_beta_search(init_board,result_board, alpha, beta, depth - 1, max_player, 1 - cur_ply_player, time_limit, total_turns_remaining - 1, eval_callback)
            if value > best_value:
                best_value = value
                best_move = move
            alpha = max(alpha, value)
            if value >= beta:
                break
        return best_move, best_value
    else:
        best_move = None
        best_value = float('inf')
        for move, result_board in genall_groupmove_resultboard(ply_board, cur_ply_player):
            _, value = alpha_beta_search(init_board,result_board, alpha, beta, depth - 1, max_player, 1 - cur_ply_player, time_limit, total_turns_remaining - 1, eval_callback)
            if value < best_value:
                best_value = value
                best_move = move
            beta = min(beta, value)
            if value <= alpha:
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

if __name__ == "__main__":
    # def f8_alt(x):
    #     return "%14.9f" % x
    #
    # import pstats
    # pstats.f8 = f8_alt

    in_base = "data/in/"
    out_base = "data/out/"
    import external

    test_num = 2
    board_marbles, player_color = external.in_to_marbles(f"{in_base}Test{test_num}.input")
    #result = genall_groupmove_resultboard(board_marbles, player_color)
    iterative_deepening_alpha_beta_search(board_marbles, 0, 10000, 15)
