import math
import threading
import tkinter as tk


class GameGUI(tk.Frame):
    DEFAULT_CONFIG = {
        'board_layout': 'standard',
        'color_selection': 'black',
        'game_move_limit': 10,
        'move_time_limit': 30,
    }
    CIRCLE_RADIUS = 30
    COLUMNS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
    BOARD_LAYOUTS = {
        'standard': {
            'white': ['i5', 'i6', 'i7', 'i8', 'i9',
                      'h4', 'h5', 'h6', 'h7', 'h8', 'h9',
                      'g5', 'g6', 'g7'],
            'black': ['a1', 'a2', 'a3', 'a4', 'a5',
                      'b1', 'b2', 'b3', 'b4', 'b5', 'b6',
                      'c3', 'c4', 'c5'],
        },
        'belgian daisy': {
            'white': [
                'i5', 'i6',
                'h4', 'h5', 'h6',
                'g4', 'g5',
                'a4', 'a5',
                'b4', 'b5', 'b6',
                'c5', 'c6'],
            'black': [
                'i8', 'i9',
                'h7', 'h8', 'h9',
                'g7', 'g8',
                'a1', 'a2',
                'b1', 'b2', 'b3',
                'c2', 'c3'],
        },
        'german daisy': {
            'white': [
                'h4', 'h5',
                'g3', 'g4', 'g5',
                'f3', 'f4',
                'b5', 'b6',
                'c5', 'c6', 'c7',
                'd6', 'd7'],
            'black': [
                'h8', 'h9',
                'g7', 'g8', 'g9',
                'f7', 'f8',
                'b1', 'b2',
                'c1', 'c2', 'c3',
                'd2', 'd3'],
        },
    }
    ai_test_action = {
        'standard': {
            'white': ['h4-g4','g5h5i5-f5g5h5', 'g6h6i6-f6g6h6','h8h9-g8g9', 'i8i9-h8h9'],
            'black': ['b1-c2','a2b2c2-b2c2d2','c3c4c5-d4d5d6','b2b3b4-c3c4c5','b3b4b5-c3c4c5'],
        },'belgian daisy': {
            'white': ['g4g5-f4f5','h4h5h6-g4g5g6','i5i6-h5h6','c5b5a5-d5b5a5','a4b4-b4c4'],
            'black': ['c2c3-d3d4','b1b2b3-c2c3c4','a1a2-b2b3','g7g8-f6f7','h9-g8'],
        },'german daisy':{
            'white': ['f3f4-f4f5','g3g4g5-g4g5g6','h4h5-h5h6','d6-e6','d7-e7'],
            'black': ['d3-d4','d2-d3','c1c2c3-c2c3c4','b2-b3','b1-b2'],
        }
    }

    def __init__(self, parent, controller, config_options):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Config setup
        self.config = config_options if config_options is not None else (
            GameGUI.DEFAULT_CONFIG)

        # Game info
        self.positions = {}
        self.player_turn = 'black'
        self.timer_running = {
            'white': False,
            'black': False,
        }
        self.num_moves = {
            'white': self.config['game_move_limit'],
            'black': self.config['game_move_limit']
        }
        self.time_left = {
            'white': self.config['move_time_limit'],
            'black': self.config['move_time_limit']
        }
        self.total_move_number = self.config['game_move_limit']

        # hard code AI moves: only for test purpose
        player_color = self.config['color_selection']
        ai_color = 'black' if player_color == 'white' else 'white'
        self.actions = self.ai_test_action[self.config['board_layout']][ai_color]
        self.current_action_index = 0

        # not updated yet
        self.white_loss = 0
        self.black_loss = 0

        # Draw the GUI
        self.draw_gui()

    def draw_gui(self):
        # Game Board Frame
        self.board_frame = tk.Frame(self, width=400, height=400, bg="white")
        self.board_frame.grid(row=1, column=1, rowspan=3)

        # Create a canvas widget
        self.canvas = tk.Canvas(self.board_frame, width=600, height=600,
                                bg="lightgrey")
        self.canvas.pack()

        # Player turn label
        self.turn_var = tk.StringVar()
        self.turn_var.set("Player turn:")
        self.turn_label = tk.Label(self, textvariable=self.turn_var)
        self.turn_label.grid(row=0, column=0)

        # Player game move limit label
        self.move_var = tk.StringVar()
        self.move_var.set(f"Moves left:")
        self.move_label = tk.Label(self, textvariable=self.move_var)
        self.move_label.grid(row=0, column=1)

        # Player time limit label
        self.time_var = tk.StringVar()
        self.time_var.set(f"Time left: {self.time_left[self.player_turn]}")
        self.time_label = tk.Label(self, textvariable=self.time_var)
        self.time_label.grid(row=0, column=2)

        # Log Information Frame
        self.log_frame = tk.Frame(self, width=100, height=400)
        self.log_frame.grid(row=1, column=2, rowspan=3)

        # Score Label
        self.white_score_label = tk.Label(self.log_frame, text=f"White Loss: {self.white_loss}")
        self.white_score_label.pack(side=tk.TOP, anchor=tk.W)
        self.black_score_label = tk.Label(self.log_frame, text=f"Black Loss: {self.black_loss}")
        self.black_score_label.pack(side=tk.TOP, anchor=tk.W)

        # Log Label
        self.log_label = tk.Label(self.log_frame, text="Logs:")
        self.log_label.pack(side=tk.TOP, anchor=tk.W)

        # Log Information Text
        self.log_text = tk.Text(self.log_frame, height=40, width=20)
        self.log_text.pack()

        # Button Frame
        self.button_frame = tk.Frame(self)
        self.button_frame.grid(row=4, column=1, columnspan=2, pady=10)

        # Reset Button
        self.reset_button = tk.Button(self.button_frame, text="Reset",
                                      command=self.reset_game)
        self.reset_button.grid(row=0, column=0, padx=5)

        # Undo Button
        self.undo_button = tk.Button(self.button_frame, text="Undo Last Move",
                                     command=self.undo_last_move)
        self.undo_button.grid(row=0, column=1, padx=5)

        # Resume Button
        self.resume_button = tk.Button(self.button_frame, text="Resume",
                                     command=self.start_turn, state="disabled")
        self.resume_button.grid(row=0, column=2, padx=5)

        # Input Action Label
        self.input_label = tk.Label(self.button_frame, text="Input Action:", state="disabled")
        self.input_label.grid(row=1, column=0, padx=5)

        # Action Entry
        self.action_entry = tk.Entry(self.button_frame)
        self.action_entry.grid(row=1, column=1, padx=5)
        self.action_entry.bind("<Return>", lambda _: self.action_entry_callback())

        # Start Button
        self.start_button = tk.Button(self, text="Start", command=self.start)
        self.start_button.grid(row=4, column=0, pady=5)

        # Back Button
        back_button = tk.Button(self, text="Back",
                                command=lambda: self.controller.display_config())
        back_button.grid(row=4, column=2, pady=5)
        self.draw_game_board()

    def action_entry_callback(self):
        self.execute_action(self.action_entry.get())
        self.action_entry.delete(0, tk.END)

    def draw_game_board(self):
        r = GameGUI.CIRCLE_RADIUS
        cols = GameGUI.COLUMNS
        for i in range(9):
            for j in range(-4, 5):
                if (abs(j) >= i or i < 9 - abs(j)):
                    x = 40 + (2 * i + 1) * r + abs(j) * r
                    y = 300 - r * j * math.sqrt(3)
                    k = j if j > 0 else 0
                    key = f'{cols[j + 4]}{i + 1 + k}'  # Construct the key string
                    # Set the values for x0, x1, y0, y1, and color for each key
                    color_value = "lightgrey"
                    if key in GameGUI.BOARD_LAYOUTS[self.config['board_layout']]['black']:
                        color_value = 'black'
                    elif key in GameGUI.BOARD_LAYOUTS[self.config['board_layout']]['white']:
                        color_value = 'white'
                    self.positions[key] = {
                        'x': x,
                        'y': y,
                        'color': color_value,
                        'id': self.canvas.create_oval(
                            x - r, y - r, x + r, y + r,
                            fill=color_value
                        )
                    }
                    self.canvas.create_text(x, y, text=key)

    def display_moved_marbles(self, input_action):
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

    def update_display(self):
        self.turn_var.set("Player turn: " + self.player_turn)
        self.move_var.set(f"Moves left: {self.num_moves[self.player_turn]}")

    def start_timer(self):
        self.timer_running[self.player_turn] = True
        self.display_time()

    def display_time(self, *args):
        print(f"updating time display for {self.player_turn}")
        if self.timer_running[self.player_turn] and self.time_left[self.player_turn] > 0:
            self.after(1000, self.display_time)
            self.time_left[self.player_turn] -= 1
            self.time_var.set(f"Time left: {self.time_left[self.player_turn]}")

    def stop_timer(self):
        self.timer_running[self.player_turn] = False

    def start(self):
        self.update_display()
        self.start_turn()

    def start_turn(self):
        self.resume_button.config(state="disabled")
        if self.total_move_number > 0:
            print("starting turn")
            self.start_timer()

            if self.config['color_selection'] != self.player_turn:
                print('Computer turn')
                self.action_entry.config(state="disabled")
                action = self.actions[self.current_action_index]
                self.current_action_index += 1
                timer = threading.Timer(3, lambda: self.execute_action(action))
                timer.start()
            else:
                print('Human turn')
                self.action_entry.config(state="normal")

    def execute_action(self, action):
        # Move marbles
        self.display_moved_marbles(action)
        # Update log information with action
        self.log_text.insert(tk.END, f"{self.player_turn.title()}:{action}\n")
        # Complete turn
        self.num_moves[self.player_turn] -= 1
        print("end turn")
        self.stop_timer()
        self.player_turn = "black" if self.player_turn == "white" else "white"
        self.update_display()
        self.start_turn()

    def undo_last_move(self):
        content = self.log_text.get("1.0", tk.END)
        lines = content.split("\n")
        last_log = ""
        last_line_index = 0
        for line in reversed(lines):
            last_line_index += 1
            # Check if the line is not empty
            if line.strip():
                last_log = line.strip()
                break
        a,last_action = last_log.split(":")
        source, destination = last_action.split("-")
        input_action = f"{destination}-{source}"
        self.display_moved_marbles(input_action)
        # Delete the last log from the text widget
        if last_line_index > 0:
            self.log_text.delete(f"end-{last_line_index-1}l",tk.END)
            self.log_text.insert(tk.END,"\n")
        # Reset turns
        self.player_turn = "black" if self.player_turn == "white" else "white"
        self.num_moves[self.player_turn] += 1
        self.update_display()
        self.resume_button.config(state="normal")
        # if self.config['color_selection'] != self.player_turn:
        #     self.current_action_index -= 1
        # self.start_turn()

    def reset_game(self):
        # Reset

        # Clear log information
        self.log_text.delete(1.0, tk.END)

