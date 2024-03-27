"""Runs a full versus simulation using 2 sets of heuristics."""
from .base_simulation import Simulation


class VersusSimulation(Simulation):

    def __init__(self):
        super().__init__()

    def start(self):
        """Starts the simulation"""
        self.update_display()