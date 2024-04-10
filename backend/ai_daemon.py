from multiprocessing import Process
from pprint import pprint

from heuristics import cam_heuristic
from statespace.search import iterative_deepening_alpha_beta_search


class AIDaemon(Process):
    def __init__(self, frontend_conn):
        super(AIDaemon, self).__init__()
        self.daemon = True
        self.frontend_conn = frontend_conn

    def run(self):
        print("Starting AI Daemon")
        while True:
            game_state = self.frontend_conn.recv()
            print('backend received the following request: ')
            pprint(game_state)

            strategy = cam_heuristic.eval_state

            move, _, elapsed_time = iterative_deepening_alpha_beta_search(
                eval_callback=strategy,
                **game_state
            )

            self.frontend_conn.send((move, elapsed_time))
