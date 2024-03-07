import tkinter as tk
from main_page import GameGUI
from config_page import ConfigGUI


class GameApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.container = tk.Frame(self, bg="white")
        self.container.grid(row=0, column=0)
        self.title("Abalone")
        self.display_game()  # to set the window height/width
        self.display_config()

    def display_config(self):
        config_gui = ConfigGUI(self.container, self)
        config_gui.grid(row=0, column=0, sticky="nsew")
        config_gui.tkraise()

    def display_game(self, config_options=None):
        game_gui = GameGUI(self.container, self, config_options)
        game_gui.grid(row=0, column=0, sticky="nsew")
        game_gui.tkraise()


app = GameApp()
app.mainloop()
