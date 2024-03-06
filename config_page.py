import tkinter as tk
from tkinter import ttk


class ConfigGUI(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # Title
        label = tk.Label(self, text="ABALONE")
        label.grid(row=0, column=0)

        # Layout selection dropdown
        layout_selection_label = tk.Label(self, text="Layout Selection:")
        layout_selection_label.grid(row=1, column=0)
        layout_selection_options = ['Standard', 'German daisy', 'Belgian daisy']

        layout_dropdown = tk.StringVar(self)
        layout_dropdown.set(layout_selection_options[0])
        layout_dropdown_menu = ttk.Combobox(self,
                                     textvariable=layout_dropdown,
                                     values=layout_selection_options,
                                     state='readonly')
        layout_dropdown_menu.grid(row=2, column=0)

        # Color selection dropdown
        color_selection_label = tk.Label(self, text="Color Selection:")
        color_selection_label.grid(row=3, column=0)
        color_selection_options = ['Black', 'White']

        color_dropdown = tk.StringVar(self)
        color_dropdown.set(color_selection_options[0])
        color_dropdown_menu = ttk.Combobox(self,
                                     textvariable=color_dropdown,
                                     values=color_selection_options,
                                     state='readonly')
        color_dropdown_menu.grid(row=4, column=0)

        # Game move limit label
        config_label = tk.Label(self, text="Move Limit:")
        config_label.grid(row=5, column=0)

        config_entry = tk.Entry(self)
        config_entry.insert(0, '10')
        config_entry.grid(row=6, column=0)

        # Start Game
        start_game_button = tk.Button(self, text="Start Game", command=
        lambda: controller.display_game({
            'board_layout': layout_dropdown.get().lower(),
            'color_selection': color_dropdown.get().lower(),
            'game_move_limit': int(config_entry.get().lower()),
        }))
        start_game_button.grid(row=7, column=0, pady=5)
