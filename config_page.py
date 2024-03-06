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
        layout_selection_options = ['Standard', 'Belgian daisy', 'German daisy']

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
        move_limit_label = tk.Label(self, text="Move Limit:")
        move_limit_label.grid(row=5, column=0)

        move_limit_entry = tk.Entry(self)
        move_limit_entry.insert(0, '10')
        move_limit_entry.grid(row=6, column=0)

        # Time move limit label
        time_limit_label = tk.Label(self, text="Time Limit per Move:")
        time_limit_label.grid(row=5, column=0)

        time_limit_entry = tk.Entry(self)
        time_limit_entry.insert(0, '30')
        time_limit_entry.grid(row=6, column=0)

        # Start Game
        start_game_button = tk.Button(self, text="Start Game", command=
        lambda: controller.display_game({
            'board_layout': layout_dropdown.get().lower(),
            'color_selection': color_dropdown.get().lower(),
            'game_move_limit': int(move_limit_entry.get()),
            'move_time_limit': int(time_limit_entry.get())
        }))
        start_game_button.grid(row=7, column=0, pady=5)
