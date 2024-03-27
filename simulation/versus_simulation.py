"""Classes and methods to simulate 2 sets of heuristics competing."""
import time

from .base_simulation import Simulation


class VersusSimulation(Simulation):
    """Runs a full versus simulation using 2 sets of heuristics."""
    def __init__(self):
        super().__init__()

    def start(self):
        """Starts the simulation"""
        self.board_state[11] = 0
        self.update_display()
        time.sleep(1)

        self.board_state[12] = 0
        self.update_display()
        time.sleep(1)

        self.board_state[13] = 0
        self.update_display()
        time.sleep(1)

        while True:
            self.update_display()
