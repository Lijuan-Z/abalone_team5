import tkinter as tk
from tkinter import ttk


class ConfigGUI(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # Title
        label = tk.Label(self, text="ABALONE")
        label.grid(row=0, column=0)

        # Dropdown Label
        config_label = tk.Label(self, text="Layout Selection:")
        config_label.grid(row=1, column=0)

        # Dropdown Options
        options = ['Standard', 'German daisy', 'Belgian daisy']

        # Dropdown
        dropdown_var = tk.StringVar(self)
        dropdown_var.set(options[0])
        dropdown_menu = ttk.Combobox(self,
                                     textvariable=dropdown_var,
                                     values=options,
                                     state='readonly')
        dropdown_menu.grid(row=2, column=0)

        config_options = {
            'board_layout': dropdown_var.get()
        }

        # Start Game
        start_game_button = tk.Button(self, text="Start Game", command=
        lambda: controller.display_game(config_options))
        start_game_button.grid(row=3, column=0, pady=5)
