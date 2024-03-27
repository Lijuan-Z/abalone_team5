"""Abstract simulation class."""
import abc
from typing import Callable


class Simulation(abc.ABC):
    def bind_display_callback(self,
                              set_display_callback: Callable[
                                  [dict[int, int]], None
                              ]):
        """Binds a display callback for the versus simulation."""
        self.board_state = {}
        self.set_display_callback = set_display_callback

    def update_display(self):
        """Updates the display with the current board state using callback."""
        self.set_display_callback(self.board_state)

    @abc.abstractmethod
    def start(self):
        """Starts the simulation"""
        pass
