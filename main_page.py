import math
import tkinter as tk
from tkinter import ttk
import config_page


class GameGUI(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # Game Board Frame
        self.board_frame = tk.Frame(self, width=400, height=400, bg="white")
        self.board_frame.grid(row=0, column=1, rowspan=3)

        # Create a canvas widget
        self.canvas = tk.Canvas(self.board_frame, width=600, height=600,
                                bg="lightgrey")
        self.canvas.pack()

        # Draw circles based on configuration
        # todo: pass configurations
        # Initialize an empty dictionary
        self.positions = {}
        self.draw_game_board()

        # Log Information Frame
        self.log_frame = tk.Frame(self, width=100, height=400, bg="lightgrey")
        self.log_frame.grid(row=0, column=2, rowspan=3)

        # Log Label
        self.log_label = tk.Label(self.log_frame, text="Logs")
        self.log_label.pack()

        # Log Information Text
        self.log_text = tk.Text(self.log_frame, height=10, width=20)
        self.log_text.pack()

        # Button Frame
        self.button_frame = tk.Frame(self)
        self.button_frame.grid(row=3, column=1, columnspan=2, pady=10)

        # Reset Button
        self.reset_button = tk.Button(self.button_frame, text="Reset",
                                      command=self.reset_game)
        self.reset_button.grid(row=0, column=0, padx=5)

        # Undo Button
        self.undo_button = tk.Button(self.button_frame, text="Undo Last Move",
                                     command=self.undo_last_move)
        self.undo_button.grid(row=0, column=1, padx=5)

        # Input Action Label
        self.input_label = tk.Label(self.button_frame, text="Input Action:")
        self.input_label.grid(row=1, column=0, padx=5)

        # Action Entry
        self.action_entry = tk.Entry(self.button_frame)
        self.action_entry.grid(row=1, column=1, padx=5)
        self.action_entry.bind("<Return>", self.set_action)

        # Configuration Label
        self.config_label = tk.Label(self, text="Move Limit:")
        self.config_label.grid(row=0, column=0)

        # Configuration Entry
        self.config_entry = tk.Entry(self)
        self.config_entry.grid(row=1, column=0, pady=10)

        # Dropdown Label
        self.config_label = tk.Label(self, text="Layout Selection:")
        self.config_label.grid(row=2, column=0)

        # Dropdown Options
        self.options = ['Standard', 'German daisy', 'Belgian daisy']

        # Dropdown
        self.dropdown_var = tk.StringVar(self)
        self.dropdown_var.set(self.options[0])
        self.dropdown_menu = ttk.Combobox(self,
                                          textvariable=self.dropdown_var,
                                          values=self.options)
        self.dropdown_menu.grid(row=3, column=0)

        # Start Button
        self.start_button = tk.Button(self, text="Start", command=self.start)
        self.start_button.grid(row=4, column=0, pady=5)

        # Back Button
        back_button = tk.Button(self, text="Back",
                                command=lambda: controller.display_config())
        back_button.grid(row=4, column=2, pady=5)

    def reset_game(self):
        # Reset

        # Clear log information
        self.log_text.delete(1.0, tk.END)

    def undo_last_move(self):
        print("undo_last_move")
        # Update log information
        # self.log_text.insert(tk.END, "Undo?\n")

    def set_action(self, event):
        # Set the action on user input
        input_action = self.action_entry.get()
        source, destination = input_action.split("-")
        source_key_list = []
        for i in range(int(len(source) / 2), 0, -1):
            source_key = source[(i - 1) * 2:2 * i]
            source_key_list.append(source_key)
            destination_key = destination[(i - 1) * 2:2 * i]
            color = self.positions[source_key]['color']
            # Update the color of the destination and the source
            self.positions[destination_key]['color'] = color
            self.canvas.itemconfig(self.positions[destination_key]['id'], fill=color)
        for source_key in source_key_list:
            if source_key not in destination:
                self.positions[source_key]['color'] = "lightgrey"
                self.canvas.itemconfig(self.positions[source_key]['id'], fill="lightgrey")

        # Update log information with action entered by the user
        self.log_text.insert(tk.END, f"Action: {input_action}\n")

    def draw_game_board(self):
        r = 30
        cols = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
        for i in range(9):
            for j in range(-4, 5):
                if (abs(j) >= i or i < 9 - abs(j)):
                    x = 40 + (2 * i + 1) * r + abs(j) * r
                    y = 300 - r * j * math.sqrt(3)
                    key = f'{cols[j + 4]}{i + 1}'  # Construct the key string
                    # Set the values for x0, x1, y0, y1, and color for each key
                    color_value = "lightgrey"
                    if cols[j + 4] == 'a' or cols[
                        j + 4] == 'b' or key == 'c3' or key == 'c4' or key == 'c5':
                        color_value = 'black'
                    if cols[j + 4] == 'h' or cols[
                        j + 4] == 'i' or key == 'g3' or key == 'g4' or key == 'g5':
                        color_value = 'white'
                    self.positions[key] = {
                        'x0': x - r,
                        'x1': x + r,
                        'y0': y - r,
                        'y1': y + r,
                        'color': color_value
                    }
                    # self.canvas.create_text(x, y, text=key)

        for key in self.positions:
            x0, y0 = self.positions[key]['x0'], self.positions[key]['y0']
            x1, y1 = self.positions[key]['x1'], self.positions[key]['y1']
            self.positions[key]['id'] = self.canvas.create_oval(x0, y0, x1, y1,
                                                                fill=
                                                                self.positions[
                                                                    key][
                                                                    'color'])

    def start(self):
        try:
            move_limit = int(self.config_entry.get())
            if move_limit > 0:
                self.draw_game_board()
            else:
                raise ValueError("Number of move must be positive")
        except ValueError:
            self.log_text.insert(tk.END, "Invalid input for number of move!\n")

        selected_option = self.dropdown_var.get()
        # self.log_text.insert(tk.END, f"Selected option: {selected_option}\n")
        print(f"Selected option: {selected_option}\n")
