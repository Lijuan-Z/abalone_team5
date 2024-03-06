import tkinter as tk


class ConfigGUI(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.config_frame = tk.Frame(self, width=510, height=410)
        self.config_frame.grid(row=0, column=1, rowspan=3)

        label = tk.Label(self, text="Config page")
        label.grid(row=0, column=4, padx=10, pady=10)

        start_game_button = tk.Button(self, text="Start Game", command=
                            lambda: controller.display_game())
        start_game_button.grid(row=1, column=1, pady=5)
