from multiprocessing import Process
from pprint import pprint

from heuristics import cam_heuristic
from statespace.search import iterative_deepening_alpha_beta_search
from statespace.transposition_table_IO import save_transposition_table_to_json, load_transposition_table_from_json


class AIDaemon(Process):
    def __init__(self, frontend_conn):
        super(AIDaemon, self).__init__()
        self.daemon = True
        self.frontend_conn = frontend_conn
        self._transposition_table_white = load_transposition_table_from_json('transposition_table_white.json')
        self._transposition_table_black = load_transposition_table_from_json('transposition_table_black.json')

    def run(self):
        print("Starting AI Daemon")
        while True:
            game_state = self.frontend_conn.recv()
            print('backend received the following request: ')
            pprint(game_state)

            strategy = cam_heuristic.eval_state
            if game_state['player'] == 0:
                move, self._transposition_table_black, elapsed_time = iterative_deepening_alpha_beta_search(
                    eval_callback=strategy,
                    transposition_table=self._transposition_table_black,
                    **game_state
                )
                self.frontend_conn.send((move, elapsed_time))

                # save_transposition_table_to_json(self._transposition_table_black, 'transposition_table_black.json')
            else:
                move, self._transposition_table_white, elapsed_time = iterative_deepening_alpha_beta_search(
                    eval_callback=strategy,
                    transposition_table=self._transposition_table_white,
                    **game_state
                )
                self.frontend_conn.send((move, elapsed_time))
                # save_transposition_table_to_json(self._transposition_table_white, 'transposition_table_white.json')
