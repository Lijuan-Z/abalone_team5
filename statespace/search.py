import random
import threading
import time
from datetime import datetime

from statespace.statespace import genall_groupmove_resultboard
import hashlib

# A dictionary of unique 64-bit integer hashes representing each position paired with each color marble.
hashed_positions = {
    (11, 0): 13694894272781220920,
    (11, 1): 14607039107576160046,
    (12, 0): 12693709892929482551,
    (12, 1): 14493725204674845980,
    (13, 0): 11463203676548433993,
    (13, 1): 18119213271117620939,
    (14, 0): 12359495938082685099,
    (14, 1): 10412403109875354847,
    (15, 0): 11116999094423638997,
    (15, 1): 12150243862170747151,
    (21, 0): 12924681918484655797,
    (21, 1): 11460965234069326014,
    (22, 0): 12034386495406519413,
    (22, 1): 10780227088564826482,
    (23, 0): 11938960601893694590,
    (23, 1): 14559619112162024852,
    (24, 0): 12232685022164288258,
    (24, 1): 9875891702377579582,
    (25, 0): 14654392472509107081,
    (25, 1): 13358677899696600539,
    (26, 0): 12153802851024297893,
    (26, 1): 10062673996909594318,
    (31, 0): 17521372971143704899,
    (31, 1): 12565724512120934967,
    (32, 0): 11821228883889561801,
    (32, 1): 10218092236808665008,
    (33, 0): 17755735723983079772,
    (33, 1): 16253821213361971047,
    (34, 0): 16479631650207109549,
    (34, 1): 16386544523088318590,
    (35, 0): 18046362236802915088,
    (35, 1): 17388189481887055607,
    (36, 0): 12671202431223526318,
    (36, 1): 11659524893831386992,
    (37, 0): 14130363149572028113,
    (37, 1): 13085015433835658608,
    (41, 0): 9609044535182176963,
    (41, 1): 14997787664625683825,
    (42, 0): 10525711761213278941,
    (42, 1): 14356888956056927290,
    (43, 0): 11803411845767890849,
    (43, 1): 10506452118256834726,
    (44, 0): 15381994817000786653,
    (44, 1): 16481497618897519253,
    (45, 0): 15975865661950339105,
    (45, 1): 12630409121559008957,
    (46, 0): 18086399558477619936,
    (46, 1): 16889673582640689356,
    (47, 0): 14570407359895287152,
    (47, 1): 10697825034959218660,
    (48, 0): 16634895313163162297,
    (48, 1): 16688963933093932103,
    (51, 0): 17930831120325885116,
    (51, 1): 16375987739413826343,
    (52, 0): 12272734712569918672,
    (52, 1): 14657744075201167989,
    (53, 0): 17811549194283030582,
    (53, 1): 12694297780214549867,
    (54, 0): 18039369183295143761,
    (54, 1): 16554795969378939497,
    (55, 0): 17750751474568372118,
    (55, 1): 9558513512501281427,
    (56, 0): 14669047322159990786,
    (56, 1): 15499610380008052736,
    (57, 0): 16227950822117312602,
    (57, 1): 9579918655293445651,
    (58, 0): 13481733623910160457,
    (58, 1): 13565261466864723296,
    (59, 0): 9791893759840836333,
    (59, 1): 17679845650462314898,
    (62, 0): 13597273410557151150,
    (62, 1): 17124689689321909696,
    (63, 0): 11871795971716157665,
    (63, 1): 10948423374857701664,
    (64, 0): 17653915202736172726,
    (64, 1): 14755599962027521720,
    (65, 0): 13534909953928563610,
    (65, 1): 14645545458582298826,
    (66, 0): 16457188899270023974,
    (66, 1): 17085927068508068243,
    (67, 0): 17995808181362736213,
    (67, 1): 12829123630851451409,
    (68, 0): 9472541027303409184,
    (68, 1): 10311951967998793383,
    (69, 0): 9933732719256774259,
    (69, 1): 9945103606825254368,
    (73, 0): 14904677903008461176,
    (73, 1): 18373506872902009240,
    (74, 0): 13357699899619609047,
    (74, 1): 10391849480190001304,
    (75, 0): 12548168994326596983,
    (75, 1): 10966963903587073077,
    (76, 0): 11110414072760217765,
    (76, 1): 12239628134674514448,
    (77, 0): 14375377289524518524,
    (77, 1): 11120810800425461820,
    (78, 0): 10804273848964161440,
    (78, 1): 16867361814729927085,
    (79, 0): 16702681525347858181,
    (79, 1): 12167884145219344782,
    (84, 0): 15933121772490062877,
    (84, 1): 9780219023090179513,
    (85, 0): 16104918890775603883,
    (85, 1): 12566099435282393223,
    (86, 0): 16489877483690276183,
    (86, 1): 18124582226366132624,
    (87, 0): 15899646159992549596,
    (87, 1): 9824628651409526889,
    (88, 0): 17513049418760900999,
    (88, 1): 12045723817283264809,
    (89, 0): 15979904495216373935,
    (89, 1): 13434488723735840853,
    (95, 0): 13055796027323318259,
    (95, 1): 15903220087263454271,
    (96, 0): 13062438335302049215,
    (96, 1): 10739631755291793903,
    (97, 0): 14099345540809372355,
    (97, 1): 17284072150546910608,
    (98, 0): 12935508047823904349,
    (98, 1): 10049904970226576526,
    (99, 0): 12041852297255749268,
    (99, 1): 17104206928422623240
}

# maps a board hash to the value calculated by the evaluation function
# transposition_table = {}

first_moves_dict = {
    # Belgian Daisy First moves
    (1835253602899219050, 1): (((11, 0), (22, 0), (33, 0)), 11),
    (1835253602899219050, 2): (((99, 0), (88, 0), (77, 0)), -11),
    (1835253602899219050, 3): (((98, 0), (87, 0)), -11),
    (1835253602899219050, 4): (((32, 0), (33, 0)), 11),
    (1835253602899219050, 5): (((23, 0), (33, 0)), 11),
    (1835253602899219050, 6): (((12, 0), (23, 0)), 11),
    (1835253602899219050, 7): (((78, 0), (77, 0)), -1),
    (1835253602899219050, 8): (((78, 0), (77, 0)), -11),
    (1835253602899219050, 9): (((21, 0), (32, 0)), 11),
    (1835253602899219050, 10): (((89, 0), (78, 0)), -11),

    # German Daisy First Moves
    (5214771994522690999, 1): (((21, 0), (32, 0), (43, 0)), 11),
    (5214771994522690999, 2): (((89, 0), (78, 0), (67, 0)), -11),
    (5214771994522690999, 3): (((42, 0), (43, 0)), 11),
    (5214771994522690999, 4): (((21, 0), (22, 0)), 1),
    (5214771994522690999, 5): (((31, 0), (42, 0)), 11),
    (5214771994522690999, 6): (((79, 0), (68, 0)), -11),
    (5214771994522690999, 7): (((88, 0), (77, 0)), -11),
    (5214771994522690999, 8): (((22, 0), (33, 0)), 11),
    (5214771994522690999, 9): (((68, 0), (67, 0)), -1),
    (5214771994522690999, 10): (((42, 0), (43, 0)), 1),

    # Standard Board First Moves
    (2251738777944622381, 1): (((11, 0), (22, 0), (33, 0)), 11),
    (2251738777944622381, 2): (((15, 0), (25, 0), (35, 0)), 10),
    (2251738777944622381, 3): (((12, 0), (23, 0), (34, 0)), 11),
    (2251738777944622381, 4): (((13, 0), (24, 0), (35, 0)), 11),
    (2251738777944622381, 5): (((14, 0), (24, 0), (34, 0)), 10),
    (2251738777944622381, 6): (((14, 0), (25, 0)), 11),
    (2251738777944622381, 7): (((12, 0), (22, 0)), 10),
    (2251738777944622381, 8): (((33, 0), (34, 0), (35, 0)), 11),
    (2251738777944622381, 9): (((33, 0), (34, 0), (35, 0)), 10),
    (2251738777944622381, 10): (((24, 0), (34, 0)), 10)
}


def iterative_deepening_alpha_beta_search(board, player, time_limit, turns_remaining, eval_callback,
                                          transposition_table, is_first_move=False, t_table_filename="transposition_table.json"):
    """
    Makes calls to alpha_beta_search, incrementing the depth each loop.

    Each call returns the best move for the given player given that depth of search. The function will continue to
    search deeper, unless the time limit is reached.

    Parameters:
        board: a dict representation of the marbles on the board
        time_limit: the total allotted time for this move to be determined in milliseconds. Should be accurate to 1/100th of a second
        player: a value, 0 or 1, indicating whose turn it is
        turns_remaining: the total remaining turns for the current player
        transposition_table: a transition table containing a board mapped to that board's evaluation
        is_first_move: a boolean indicating if this is the first move of the game. Used to pick from a list of random first moves.
        t_table_filename: Name of the file to load the t_table from if it has yet to be loaded
    Returns:
        best_move: the best move found from all iterations the alpha-beta search
    """

    if is_first_move and player == 0:
        first_move = first_moves_dict[(hash_board_state(board), random.randint(1, 10))]
        print(f"First Move: {first_move}")
        return first_move, transposition_table, 0

    start_time = datetime.now()
    depth = 1
    total_turns_remaining = turns_remaining * 2 - player
    best_move = None
    best_index = None
    cur_path = []
    elapsed_time = 0
    best_move_search_time = 0
    time_limit_seconds = time_limit / 1000.0  # Convert time_limit to seconds for comparison

    careful_thresh_seconds = time_limit_seconds * 0.05 # if an iteration is started past this time, it will be a careful search
    full_cutoff_thresh_seconds = time_limit_seconds - 0.1

    # The loop will end before the time limit if the maximum depth (based on turns remaining) is reached.
    while depth <= total_turns_remaining:
        elapsed_time = (datetime.now() - start_time).total_seconds()

        temp_move = None
        temp_index = None

        if elapsed_time > careful_thresh_seconds:
            print("CAREFUL THRESH REACHED:")

            stop_flag = threading.Event()

            kwargs = dict(init_board=board, ply_board=board,
                          alpha=float('-inf'), beta=float('inf'),
                          depth=depth, max_player=player, cur_ply_player=player,
                          time_limit=time_limit_seconds - elapsed_time,
                          total_turns_remaining=total_turns_remaining,
                          eval_callback=eval_callback,
                          transposition_table=transposition_table,
                          end_of_time_flag=stop_flag,
                          path=cur_path,
                          total_depth=depth
                          )

            search_thread = CarefulABThread(
                target=careful_alpha_beta_search_transposition, kwargs=kwargs
            )

            careful_search_time = full_cutoff_thresh_seconds - elapsed_time
            if careful_search_time >= 0.1:
                search_thread.start()
                print(f"{elapsed_time}s, Attempting careful search for an additional {careful_search_time} seconds")
                print(f"beginning careful search for {careful_search_time} seconds")
                time.sleep(careful_search_time)
                stop_flag.set()
                temp_move, temp_index, _ = search_thread.join()
            else:
                print(f"search time requested for {careful_search_time}s. no point :( ending search")


        elif elapsed_time <= careful_thresh_seconds:
            print("RECKLESS:")
            print("ELAPSED TIME:", elapsed_time)
            temp_move, temp_index, _ = reckless_alpha_beta_search_transposition(
                init_board=board, ply_board=board,
                alpha=float('-inf'), beta=float('inf'),
                depth=depth, max_player=player, cur_ply_player=player,
                time_limit=time_limit_seconds - elapsed_time,
                total_turns_remaining=total_turns_remaining,
                eval_callback=eval_callback,
                transposition_table=transposition_table,
                path=cur_path,
                total_depth=depth
            )

        elapsed_time = (datetime.now() - start_time).total_seconds()
        print("TEMP MOVE:", temp_move)

        if temp_move is not None:
            best_move = temp_move
            best_index = temp_index
            best_move_search_time = elapsed_time
            depth += 1
        else:
            depth -= 1
            break

        if cur_path[0] != best_index:
            cur_path = [best_index]

        if elapsed_time > time_limit_seconds:
            depth -= 1
            break
    print("\n=======FINISHED========")
    print(f"Best Move Search Time: {best_move_search_time * 1000:.2f}ms/{time_limit:.2f}ms")  # Display in milliseconds
    print(f"Total Elapsed Time: {elapsed_time * 1000:.2f}ms/{time_limit:.2f}ms ")
    print(f"Depth Reached: {depth}")
    print(f"Path: {cur_path}")
    print(f"Best Move: {best_move}")
    return best_move, transposition_table, elapsed_time


def iterative_deepening_alpha_beta_search_by_depth(board, player, depth, turns_remaining, eval_callback, ab_callback,
                                                   transposition_table, path,
                                                   is_first_move=False,
                                                   t_table_filename="transposition_table.json"):

    if is_first_move and player == 0:
        first_move = first_moves_dict[(hash_board_state(board), random.randint(1, 3))]
        print(f"First Move: {first_move}")
        return first_move, transposition_table

    start_time = datetime.now()
    cur_depth = 1
    cur_path = path
    best_move = None

    while cur_depth <= depth and cur_depth <= turns_remaining:
        best_move, best_index, _ = ab_callback(board, board, float('-inf'), float('inf'), cur_depth, cur_depth, player, player, 0, turns_remaining, eval_callback, transposition_table, cur_path)
        elapsed_time = (datetime.now() - start_time).total_seconds()
        if cur_path[0] != best_index:
            cur_path = [best_index]
        print("\n=======PLY FINISHED========")
        print(f"Search Time: {elapsed_time * 1000:.2f}ms")  # Display in milliseconds
        print(f"Depth: {cur_depth}")
        print(f"Best Move: {best_move}")
        print(f"Path: {cur_path}")
        cur_depth += 1

    return best_move, cur_path, transposition_table

class CarefulABThread(threading.Thread):

    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        threading.Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self, *args):
        threading.Thread.join(self, *args)
        return self._return

def careful_alpha_beta_search_transposition(end_of_time_flag, init_board, ply_board, alpha, beta, total_depth, depth, max_player, cur_ply_player, time_limit,
                                    total_turns_remaining, eval_callback, transposition_table, path = None):
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
        (best_move, best_move_index, best_value): A tuple containing the best move for a player and that move's value as determined
        by the evaluation function
    """

    if depth == 0 or total_turns_remaining == 0 or num_player_marbles(cur_ply_player, ply_board) == 8:
        board_hash = hash_board_state(ply_board)
        if transposition_table.get(board_hash) is None:
            transposition_table[board_hash] = eval_callback(init_board=init_board, ply_board=ply_board,
                                                            total_turns_remaining=total_turns_remaining,
                                                            max_player=max_player,
                                                            time_limit=time_limit)
        return None, None, transposition_table[board_hash]

    best_move = None
    best_move_index = None
    best_gm_rb = None
    continue_search = True
    x = genall_groupmove_resultboard(ply_board, cur_ply_player)
    groupmove_resultboard = sorted(x, key=lambda item: len(item[0][0]), reverse=True)
    if path is not None:
        try:
            best_gm_rb = groupmove_resultboard[path[total_depth - depth]]
            # del groupmove_resultboard[path[total_depth - depth]]
        except Exception:
            try:
                path[total_depth - depth]
            except Exception:
                path.append(None)

    if cur_ply_player == max_player:
        best_value = float('-inf')
        if best_gm_rb:

            if end_of_time_flag.is_set():
                return None, None, None

            _, _, value = careful_alpha_beta_search_transposition(end_of_time_flag, init_board, best_gm_rb[1], alpha, beta, total_depth, depth - 1, max_player, 1 - cur_ply_player, time_limit, total_turns_remaining - 1, eval_callback, transposition_table, path)

            if value is None:
                return None, None, None

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
                if end_of_time_flag.is_set():
                    return None, None, None
                _, _, value = careful_alpha_beta_search_transposition(end_of_time_flag, init_board, result_board, alpha, beta, total_depth, depth - 1, max_player, 1 - cur_ply_player, time_limit, total_turns_remaining - 1, eval_callback, transposition_table)
                if value is None:
                    return None, None, None
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
            if end_of_time_flag.is_set():
                return None, None, None
            _, _, value = careful_alpha_beta_search_transposition(end_of_time_flag, init_board, best_gm_rb[1], alpha, beta, total_depth, depth - 1, max_player, 1 - cur_ply_player, time_limit, total_turns_remaining - 1, eval_callback, transposition_table, path)
            if value is None:
                return None, None, None
            if value < best_value:
                best_value = value
                best_move = best_gm_rb[0]
                best_move_index = path[total_depth - depth]
            if value <= alpha:
                continue_search = False
            if value < beta:
                beta = value
        if continue_search is True:
            for i, (move, result_board) in enumerate(groupmove_resultboard):
                if end_of_time_flag.is_set():
                    return None, None, None
                _, _, value = careful_alpha_beta_search_transposition(end_of_time_flag, init_board, result_board, alpha, beta, total_depth, depth - 1, max_player, 1 - cur_ply_player, time_limit, total_turns_remaining - 1, eval_callback, transposition_table)
                if value is None:
                    return None, None, None
                if value < best_value:
                    best_value = value
                    best_move = move
                    best_move_index = i
                if value <= alpha:
                    break
                if value < beta:
                    beta = value

    if path and path[total_depth - depth] is None:
        path[total_depth - depth] = best_move_index
    return best_move, best_move_index, best_value

def reckless_alpha_beta_search_transposition(init_board, ply_board, alpha, beta, total_depth, depth, max_player, cur_ply_player, time_limit,
                                    total_turns_remaining, eval_callback, transposition_table, path = None):
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
        (best_move, best_move_index, best_value): A tuple containing the best move for a player and that move's value as determined
        by the evaluation function
    """

    if depth == 0 or total_turns_remaining == 0 or num_player_marbles(cur_ply_player, ply_board) == 8:
        board_hash = hash_board_state(ply_board)
        if transposition_table.get(board_hash) is None:
            transposition_table[board_hash] = eval_callback(init_board=init_board, ply_board=ply_board,
                                                            total_turns_remaining=total_turns_remaining,
                                                            max_player=max_player,
                                                            time_limit=time_limit)
        return None, None, transposition_table[board_hash]

    best_move = None
    best_move_index = None
    best_gm_rb = None
    continue_search = True
    x = genall_groupmove_resultboard(ply_board, cur_ply_player)
    groupmove_resultboard = sorted(x, key=lambda item: len(item[0][0]), reverse=True)
    if path is not None:
        try:
            best_gm_rb = groupmove_resultboard[path[total_depth - depth]]
            # del groupmove_resultboard[path[total_depth - depth]]
        except Exception:
            try:
                path[total_depth - depth]
            except Exception:
                path.append(None)

    if cur_ply_player == max_player:
        best_value = float('-inf')
        if best_gm_rb:
            _, _, value = reckless_alpha_beta_search_transposition(init_board, best_gm_rb[1], alpha, beta, total_depth, depth - 1, max_player, 1 - cur_ply_player, time_limit, total_turns_remaining - 1, eval_callback, transposition_table, path)
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
                _, _, value = reckless_alpha_beta_search_transposition(init_board, result_board, alpha, beta, total_depth, depth - 1, max_player, 1 - cur_ply_player, time_limit, total_turns_remaining - 1, eval_callback, transposition_table)
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
            _, _, value = reckless_alpha_beta_search_transposition(init_board, best_gm_rb[1], alpha, beta, total_depth, depth - 1, max_player, 1 - cur_ply_player, time_limit, total_turns_remaining - 1, eval_callback, transposition_table, path)
            if value < best_value:
                best_value = value
                best_move = best_gm_rb[0]
                best_move_index = path[total_depth - depth]
            if value <= alpha:
                continue_search = False
            if value < beta:
                beta = value
        if continue_search is True:
            for i, (move, result_board) in enumerate(groupmove_resultboard):
                _, _, value = reckless_alpha_beta_search_transposition(init_board, result_board, alpha, beta, total_depth, depth - 1, max_player, 1 - cur_ply_player, time_limit, total_turns_remaining - 1, eval_callback, transposition_table)
                if value < best_value:
                    best_value = value
                    best_move = move
                    best_move_index = i
                if value <= alpha:
                    break
                if value < beta:
                    beta = value

    if path and path[total_depth - depth] is None:
        path[total_depth - depth] = best_move_index
    return best_move, best_move_index, best_value


def alpha_beta_search_control(init_board, ply_board, alpha, beta, total_depth, depth, max_player, cur_ply_player, time_limit,
                              total_turns_remaining, eval_callback, transposition_table, path = None):
    if depth == 0 or total_turns_remaining == 0 or num_player_marbles(cur_ply_player, ply_board) == 8:
        board_hash = hash_board_state(ply_board)
        if transposition_table.get(board_hash) is None:
            transposition_table[board_hash] = eval_callback(init_board=init_board, ply_board=ply_board,
                                                            total_turns_remaining=total_turns_remaining,
                                                            max_player=max_player,
                                                            time_limit=time_limit)
        return None, None, transposition_table[board_hash]

    best_move = None
    best_move_index = None
    best_gm_rb = None
    continue_search = True
    groupmove_resultboard = genall_groupmove_resultboard(ply_board, cur_ply_player)
    if path is not None:
        try:
            best_gm_rb = groupmove_resultboard[path[total_depth - depth]]
            del groupmove_resultboard[path[total_depth - depth]]
        except Exception:
            try:
                path[total_depth - depth]
            except Exception:
                path.append(None)

    if cur_ply_player == max_player:
        best_value = float('-inf')
        if best_gm_rb:
            _, _, value = alpha_beta_search_control(init_board, best_gm_rb[1], alpha, beta, total_depth, depth - 1, max_player, 1 - cur_ply_player, time_limit, total_turns_remaining - 1, eval_callback, transposition_table, path)
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
                _, _, value = alpha_beta_search_control(init_board,result_board, alpha, beta, total_depth, depth - 1, max_player, 1 - cur_ply_player, time_limit, total_turns_remaining - 1, eval_callback, transposition_table)
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
            _, _, value = alpha_beta_search_control(init_board, best_gm_rb[1], alpha, beta, total_depth, depth - 1, max_player, 1 - cur_ply_player, time_limit, total_turns_remaining - 1, eval_callback, transposition_table, path)
            if value < best_value:
                best_value = value
                best_move = best_gm_rb[0]
                best_move_index = path[total_depth - depth]
            if value <= alpha:
                continue_search = False
            if value < beta:
                beta = value
        if continue_search is True:
            for i, (move, result_board) in enumerate(groupmove_resultboard):
                _, _, value = alpha_beta_search_control(init_board,result_board, alpha, beta, total_depth, depth - 1, max_player, 1 - cur_ply_player, time_limit, total_turns_remaining - 1, eval_callback, transposition_table)
                if value < best_value:
                    best_value = value
                    best_move = move
                    best_move_index = i
                if value <= alpha:
                    break
                if value < beta:
                    beta = value

    if path and path[total_depth - depth] is None:
        path[total_depth - depth] = best_move_index
    return best_move, best_move_index, best_value


def hash_marble_position(position, player):
    """
    Generate a 64-bit hash for a given marble position and player.

    Parameters:
    - position: The marble's position.
    - player: The player number (0 or 1).

    Returns:
    A 64-bit integer hash.
    """
    # Create a unique string representation for the position and player
    unique_string = f'{position}-{player}'.encode('utf-8')

    # Generate a SHA-256 hash of the unique string
    sha256_hash = hashlib.sha256(unique_string).digest()

    # Truncate the hash to 64 bits and convert to integer
    hash_val = int.from_bytes(sha256_hash[:8], 'big')

    # Ensure the hash uses all 64 bits by setting the 64th bit
    hash_val |= (1 << 63)
    print(hash_val.bit_length())

    return hash_val


def generate_all_hashes(valid_coords):
    """
    Generate 64-bit hashes for all valid marble positions for both players.

    Parameters:
    - valid_coords: A list of valid marble positions.

    Returns:
    A dictionary mapping each (position, player) pair to a 64-bit hash.
    """
    hash_table = {}
    for position in valid_coords:
        for player in [0, 1]:
            hash_table[(position, player)] = hash_marble_position(position, player)

    return hash_table


def hash_board_state(board):
    hashed_board = 0  # Use 0 as the initial value since X ^ 0 = X for any X
    for position, player in board.items():
        hashed_board ^= hashed_positions[(position, player)]
    return hashed_board


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
