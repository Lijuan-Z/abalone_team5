"""Interface for game simulations."""
import tkinter as tk
from .simulation_page import SimulationGUI


class SimApp(tk.Tk):
    """GameApp runs the tkinter app and controls switching between GUIs."""

    def __init__(self, *args, **kwargs):
        """Initializes a new GameApp instance.

        :param args: any args to pass through to tk.Tk
        :param kwargs: any kwargs to pass through to tk.Tk
        """

        tk.Tk.__init__(self, *args, **kwargs)

        self.container = tk.Frame(self, bg="white")
        self.container.grid(row=0, column=0)
        self.title("Abalone Simulation")
        self.display_simulation_gui()  # to set the window height/width

    def display_simulation_gui(self, config_options=None):
        """Switches to and displays the GameGUI, passing in any configs."""
        game_gui = SimulationGUI(self.container, self, config_options)
        game_gui.grid(row=0, column=0, sticky="nsew")
        game_gui.tkraise()

