""" This module holds the Game App. """
import tkinter as tk
from .main_page import GameGUI
from .config_page import ConfigGUI


class GameApp(tk.Tk):
    """GameApp runs the tkinter app and controls switching between GUIs."""

    def __init__(self, *args, **kwargs):
        """Initializes a new GameApp instance.

        :param args: any args to pass through to tk.Tk
        :param kwargs: any kwargs to pass through to tk.Tk
        """

        tk.Tk.__init__(self, *args, **kwargs)

        self.container = tk.Frame(self, bg="white")
        self.container.grid(row=0, column=0)
        self.title("Abalone")
        self.display_game()  # to set the window height/width
        self.display_config()

    def display_config(self):
        """Switches to and displays the ConfigGUI."""
        config_gui = ConfigGUI(self.container, self)
        config_gui.grid(row=0, column=0, sticky="nsew")
        config_gui.tkraise()

    def display_game(self, config_options=None):
        """Switches to and displays the GameGUI, passing in any configs."""
        game_gui = GameGUI(self.container, self, config_options)
        game_gui.grid(row=0, column=0, sticky="nsew")
        game_gui.tkraise()
