import tkinter as tk
import main_page


class ConfigGUI(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="Config page")
        label.grid(row=0, column=4, padx=10, pady=10)

        start_game_button = tk.Button(self, text="Start Game", command=
                            lambda: controller.show_frame(main_page.GameGUI))
        start_game_button.grid(row=1, column=1, padx=10, pady=10)
