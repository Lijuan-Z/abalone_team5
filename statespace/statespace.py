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
# from pprint import pprint
import debugutils

absolute_directions = [10, 11, 1]

bounds = {
    0: (5, 4),
    1: (1, 5),
    2: (1, 6),
    3: (1, 7),
    4: (1, 8),
    5: (1, 9),
    6: (2, 9),
    7: (3, 9),
    8: (4, 9),
    9: (5, 9),
    10: (5, 4)
}


def genall_groupmove_resultboard(marbles: dict[int, int],
                                 player_color: int)\
        -> list[tuple[tuple[tuple[int, int], ...], int], dict[int, int]]:
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
    debugutils.print_board(marbles)
    # print("marbles:")
    # pprint(marbles)
    # print("player_color:", player_color)

    player_marbles = dict(filter(lambda marble: marble[1] == player_color,
                                 marbles.items()))
    # print("player_marbles:")
    # pprint(player_marbles)

    inlinegroupmoves, sidestepgroupmoves = genall_groupmoves(marbles, player_marbles)

    with open("data/out/TESTOUT", 'a+') as f_board:
        for move in inlinegroupmoves:
            resultant_board = marbles.copy()
            apply_move(resultant_board, move)
            out_formatted_board = dict_to_out(resultant_board)
            f_board.write(out_formatted_board)


    # print("all_groupmoves:")
    # pprint(all_groupmoves)


def dict_to_out(board):
    out_str = ""

    board_items = board.items()
    blacks = list(filter(lambda item: item[1] == 0, board_items))
    whites = list(filter(lambda item: item[1] == 1, board_items))
    blacks.sort()
    whites.sort()

    all_marbles = blacks + whites
    for marble in all_marbles:
        # (67, 1)
        out_str += f"{chr((marble[0]//10) + 64)}{marble[0]%10}{'b' if marble[1] == 0 else 'w'},"

    return out_str[:-1] + "\n"



    print()

    # for coord, color in board.items():



    # with open(in_path, 'r') as f:
    #     player_turn = 0 if 'b' in f.readline() else 1
    #
    #     board = {}
    #     for coord in f.readline().split(','):
    #         column_digit = (ord(coord[0]) - 64)
    #         row_digit = int(coord[1])
    #         color = 0 if coord[2] == 'b' else 1
    #         board[column_digit*10 + row_digit] = color

    # return board, player_turn


def genall_groupmoves(board: dict[int, int],
                      player_marbles: dict[int, int]) \
        -> list[tuple[tuple[tuple[int, int], ...], int]]:
    """Generates all groupmoves given a dict of marbles and the current board.

    return format explained:
        list[groupmove]
    """
    inlinegroupmoves, sidestepgroupdirs = \
        genall_inlinegroupmoves_sidestepgroupdirs(board, player_marbles)
    # print("inline groupmoves:")
    # pprint(inlinegroupmoves)
    # print("sidestep groupdirs:")
    # pprint(sidestepgroupdirs)

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
        try:
            board[marble[0] + direction]
            return False
        except KeyError:
            pass

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

    # print("cur_grouping", cur_grouping)
    # print("next_coord", next_coord)

    next_marble = None

    while True:
        # if next == AVAILABLE: break
        try:
            # throws KeyError if no marble at that coordinate
            next_marble = (next_coord, board[next_coord])
        except KeyError:
            # print("terminate")
            break

        if is_out_of_bounds(next_coord) \
                or num_players == num_enemies \
                or num_players == 3 and next_marble[1] == marble[1]:
            # print("terminate")
            break

        cur_grouping.append(next_marble)
        # print(cur_grouping)

        if next_marble[1] == marble[1]:
            sidestep_groupdirs.append((tuple(cur_grouping), direction))
            num_players += 1
        elif next_marble[1] == 1 - marble[1]:
            num_enemies += 1

        next_coord += direction

    # print(sidestep_groupdirs)

    # print(type(sidestep_groupdirs[0][0][0]))
    # print(type(sidestep_groupdirs[0][0][1]))
    if is_out_of_bounds(next_coord) and cur_grouping[-1][1] == marble[1]:
        # return (None, sidestep_groupdirs)
        return None, sidestep_groupdirs
    elif num_players == 3 and next_marble and next_marble[1] == marble[1]:
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

    # print("cur_grouping", cur_grouping)
    # print("next_coord", next_coord)

    next_marble = None

    while True:
        # if next == AVAILABLE: break
        try:
            # throws KeyError if no marble at that coordinate
            next_marble = (next_coord, board[next_coord])
        except KeyError:
            # print("terminate")
            break

        if is_out_of_bounds(next_coord) \
                or num_players == num_enemies \
                or num_players == 3 and next_marble[1] == marble[1]:
            # print("terminate")
            break

        cur_grouping.append(next_marble)
        # print(cur_grouping)

        if next_marble[1] == marble[1]:
            num_players += 1
        elif next_marble[1] == 1 - marble[1]:
            num_enemies += 1

        next_coord += direction

    # print(sidestep_groupdirs)

    # print(type(sidestep_groupdirs[0][0][0]))
    # print(type(sidestep_groupdirs[0][0][1]))
    if is_out_of_bounds(next_coord) and cur_grouping[-1][1] == marble[1]:
        # return (None, sidestep_groupdirs)
        return None
    elif num_players == 3 and next_marble and next_marble[1] == marble[1]:
        return None
    elif num_players > num_enemies:
        return tuple(cur_grouping), direction
    else:
        return None


def is_out_of_bounds(marble_coord: int) -> bool:
    """True if marble coord is out of bounds of an abalone board."""
    # print(marble_coord)
    row = marble_coord // 10
    col = marble_coord % 10
    return col < bounds[row][0] or col > bounds[row][1]


def apply_move(board, groupmove):
    """Apply the given move to the given board state."""
    for marble in reversed(groupmove[0]):
        del board[marble[0]]
        new_coord = marble[0] + groupmove[1]
        if is_out_of_bounds(new_coord):
            continue
        board[marble[0] + groupmove[1]] = marble[1]
        print()



if __name__ == "__main__":
    in_base = "data/in/"
    out_base = "data/out/"
    import external

    test_num = 1
    board_marbles, player_color = external.in_to_marbles(f"{in_base}Test{test_num}.input")
    result = genall_groupmove_resultboard(board_marbles, player_color)
    print("groupmoves_resultboards:", result)
