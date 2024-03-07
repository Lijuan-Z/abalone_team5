"""This module holds the Config GUI."""
import tkinter as tk
from tkinter import ttk


class ConfigGUI(tk.Frame):
    """ConfigGUI allows user to enter configs before they begin the game."""

    ASCII = """
           _           _                  
     /\\   | |         | |                 
    /  \\  | |__   __ _| | ___  _ __   ___ 
   / /\\ \\ | '_ \\ / _` | |/ _ \\| '_ \\ / _ \\
  / ____ \\| |_) | (_| | | (_) | | | |  __/
 /_/    \\_\\_.__/ \\__,_|_|\\___/|_| |_|\\___|
 
    """

    def __init__(self, parent, controller):
        """Initializes a new ConfigUI.

        Displays a title, configuration options, and a start game button.
        :param parent: the parent frame this GUI will reside in
        :param controller: the GameApp that manages GUIs
        """

        tk.Frame.__init__(self, parent)

        content = tk.Frame(self, width=100, height=100)
        content.pack(expand=True, anchor="center")

        # Title
        label_var = tk.StringVar(content)
        label_var.set(ConfigGUI.ASCII)
        label = tk.Label(content, textvariable=label_var,
                         font=('Courier', 10, 'bold'))
        label.grid(row=0, column=0, pady=(0, 5))

        # Layout selection dropdown
        layout_selection_label = tk.Label(content, text="Board Layout:")
        layout_selection_label.grid(row=1, column=0, pady=5)
        layout_selection_options = ['Standard', 'Belgian daisy',
                                    'German daisy']

        layout_dropdown = tk.StringVar(content)
        layout_dropdown.set(layout_selection_options[0])
        layout_dropdown_menu = ttk.Combobox(content,
                                            textvariable=layout_dropdown,
                                            values=layout_selection_options,
                                            state='readonly')
        layout_dropdown_menu.grid(row=2, column=0, pady=5)

        # Color selection dropdown
        color_selection_label = tk.Label(content, text="Human Player Color:")
        color_selection_label.grid(row=3, column=0, pady=5)
        color_selection_options = ['Black', 'White']

        color_dropdown = tk.StringVar(content)
        color_dropdown.set(color_selection_options[0])
        color_dropdown_menu = ttk.Combobox(content,
                                           textvariable=color_dropdown,
                                           values=color_selection_options,
                                           state='readonly')
        color_dropdown_menu.grid(row=4, column=0, pady=5)

        # Game mode selection dropdown
        game_mode_selection_label = tk.Label(content,
                                             text="Game Mode:")
        game_mode_selection_label.grid(row=5, column=0, pady=5)
        game_mode_selection_options = ['Human vs. Computer']

        game_mode_dropdown = tk.StringVar(content)
        game_mode_dropdown.set(game_mode_selection_options[0])
        game_mode_dropdown_menu = ttk.Combobox(content,
                                               textvariable=game_mode_dropdown,
                                               values=game_mode_selection_options,
                                               state='readonly')
        game_mode_dropdown_menu.grid(row=6, column=0, pady=5)

        # Game move limit label
        move_limit_label = tk.Label(content, text="Move Limit:")
        move_limit_label.grid(row=7, column=0, pady=5)

        move_limit_entry = tk.Entry(content)
        move_limit_entry.insert(0, '10')
        move_limit_entry.grid(row=8, column=0, pady=5)

        # Time move limit label
        white_time_limit_label = tk.Label(content, text="White Time Limit per Move:")
        white_time_limit_label.grid(row=9, column=0, pady=5)

        white_time_limit_entry = tk.Entry(content)
        white_time_limit_entry.insert(0, '30')
        white_time_limit_entry.grid(row=10, column=0, pady=5)

        black_time_limit_label = tk.Label(content, text="Black Time Limit per Move:")
        black_time_limit_label.grid(row=11, column=0, pady=5)

        black_time_limit_entry = tk.Entry(content)
        black_time_limit_entry.insert(0, '30')
        black_time_limit_entry.grid(row=12, column=0, pady=5)

        # Start Game
        start_game_button = tk.Button(content, text="Start Game", command=
        lambda: controller.display_game({
            'board_layout': layout_dropdown.get().lower(),
            'color_selection': color_dropdown.get().lower(),
            'game_mode': game_mode_dropdown.get().lower(),
            'game_move_limit': int(move_limit_entry.get()),
            'black_move_time_limit': int(black_time_limit_entry.get()),
            'white_move_time_limit': int(white_time_limit_entry.get()),
        }))
        start_game_button.grid(row=13, column=0, pady=20)
