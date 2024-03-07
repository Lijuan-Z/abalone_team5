"""This module holds the Game GUI."""
import math
import random
import threading
import tkinter as tk


class GameGUI(tk.Frame):
    """GameGUI displays the game board and executes game logic."""

    DEFAULT_CONFIG = {
        'board_layout': 'standard',
        'color_selection': 'black',
        'game_mode': 'human vs. computer',
        'game_move_limit': 10,
        'black_move_time_limit': 30,
        'white_move_time_limit': 30,
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
            'white': ['h4-g4', 'g5h5i5-f5g5h5', 'g6h6i6-f6g6h6', 'h8h9-g8g9',
                      'i8i9-h8h9'],
            'black': ['b1-c2', 'a2b2c2-b2c2d2', 'c3c4c5-d4d5d6',
                      'b2b3b4-c3c4c5', 'b3b4b5-c3c4c5'],
        }, 'belgian daisy': {
            'white': ['g4g5-f4f5', 'h4h5h6-g4g5g6', 'i5i6-h5h6',
                      'c5b5a5-d5b5a5', 'a4b4-b4c4'],
            'black': ['c2c3-d3d4', 'b1b2b3-c2c3c4', 'a1a2-b2b3', 'g7g8-f6f7',
                      'h9-g8'],
        }, 'german daisy': {
            'white': ['f3f4-f4f5', 'g3g4g5-g4g5g6', 'h4h5-h5h6', 'd6-e6',
                      'd7-e7'],
            'black': ['d3-d4', 'd2-d3', 'c1c2c3-c2c3c4', 'b2-b3', 'b1-b2'],
        }
    }

    def __init__(self, parent, controller, config_options):
        """Initializes a new GameGUI and starts the game.

        Prepares the game with the given configuration options and the base
        game info, then displays the board and the necessary buttons for
        starting the game.
        :param parent: the parent frame this GUI will reside in
        :param controller: the GameApp that manages GUIs
        :param config_options: the config options to load the game with
        """

        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Config setup
        self.config = config_options if config_options is not None else (
            GameGUI.DEFAULT_CONFIG)
        print(self.config)

        # Game info
        self.positions = {}
        self.player_turn = 'black'
        self.paused = False
        self.num_moves = {
            'white': self.config['game_move_limit'],
            'black': self.config['game_move_limit']
        }
        self.time_left = {
            'white': self.config['black_move_time_limit'],
            'black': self.config['white_move_time_limit']
        }
        self.total_move_number = self.config['game_move_limit']

        # hard code AI moves: only for test purpose
        player_color = self.config['color_selection']
        ai_color = 'black' if player_color == 'white' else 'white'
        self.actions = self.ai_test_action[self.config['board_layout']][
            ai_color]
        self.current_action_index = 0
        self.ai_recommendation_history = list()

        # not updated yet
        self.white_loss = 0
        self.black_loss = 0

        # Draw the GUI and game board
        self.draw_gui()
        self.draw_game_board()

    def draw_gui(self):
        """Draws all the elements on the screen, excluding the game board."""

        # Game Board Frame
        self.board_frame = tk.Frame(self, width=400, height=400, bg="white")
        self.board_frame.grid(row=1, column=1, rowspan=3, padx=20)

        # Canvas widget
        self.canvas = tk.Canvas(self.board_frame, width=600, height=600,
                                bg="lightgrey")
        self.canvas.pack()

        # Info frame
        self.info_frame = tk.Frame(self)
        self.info_frame.grid(row=0, column=1, pady=20, columnspan=2)

        # Game state frame
        self.state_frame = tk.Frame(self.info_frame)
        self.state_frame.pack(side="left", padx=20)

        # Player turn label
        self.turn_var = tk.StringVar()
        self.turn_var.set("Player turn:")
        self.turn_label = tk.Label(self.state_frame,
                                   textvariable=self.turn_var)
        self.turn_label.pack(side=tk.TOP, anchor=tk.W)

        # State label
        self.state_var = tk.StringVar()
        self.state_var.set("NO GAME STARTED")
        self.state_label = tk.Label(self.state_frame,
                                    textvariable=self.state_var)
        self.state_label.pack(side=tk.TOP, anchor=tk.W)

        # Player game move limit label
        self.move_frame = tk.Frame(self.info_frame)
        self.move_frame.pack(side="left", padx=20)

        self.black_move_var = tk.StringVar()
        self.black_move_var.set(f"Black moves left: {self.num_moves['black']}")
        self.black_move_label = tk.Label(self.move_frame,
                                         textvariable=self.black_move_var)
        self.black_move_label.pack(side=tk.TOP, anchor=tk.W)

        self.white_move_var = tk.StringVar()
        self.white_move_var.set(f"White moves left: {self.num_moves['white']}")
        self.white_move_label = tk.Label(self.move_frame,
                                         textvariable=self.white_move_var)
        self.white_move_label.pack(side=tk.TOP, anchor=tk.W)

        # Score Label
        self.score_frame = tk.Frame(self.info_frame)
        self.score_frame.pack(side="left", padx=20)

        self.black_score_label = tk.Label(self.score_frame,
                                        text=f"Black score: {self.white_loss}")
        self.black_score_label.pack(side=tk.TOP, anchor=tk.W)
        self.white_score_label = tk.Label(self.score_frame,
                                        text=f"White score: {self.black_loss}")
        self.white_score_label.pack(side=tk.TOP, anchor=tk.W)

        # Player time limit label
        self.time_frame = tk.Frame(self.info_frame)
        self.time_frame.pack(side="left", padx=20)

        self.black_time_var = tk.StringVar()
        self.black_time_var.set(f"Black time left: {self.time_left['black']}")
        self.time_label = tk.Label(self.time_frame,
                                   textvariable=self.black_time_var)
        self.time_label.pack(side=tk.TOP, anchor=tk.W)

        self.white_time_var = tk.StringVar()
        self.white_time_var.set(f"White time left: {self.time_left['white']}")
        self.time_label = tk.Label(self.time_frame,
                                   textvariable=self.white_time_var)
        self.time_label.pack(side=tk.TOP, anchor=tk.W)

        # History Column
        self.history_column = tk.Frame(self)
        self.history_column.grid(row=1, column=2, rowspan=3, padx=(20, 30))

        # Log Information Frame
        self.log_frame = tk.Frame(self.history_column, width=100, height=100)
        self.log_frame.pack(side=tk.TOP, anchor=tk.W, pady=(0, 10))

        # Log Label
        self.log_label = tk.Label(self.log_frame, text="Logs:")
        self.log_label.pack(side=tk.TOP, anchor=tk.W)

        # Log Information Text
        self.log_text = tk.Text(self.log_frame, height=10, width=20)
        self.log_text.pack()

        # AI Recommendations Frame
        self.ai_recs_frame = tk.Frame(
            self.history_column, width=100, height=100)
        self.ai_recs_frame.pack(side=tk.TOP, anchor=tk.W, pady=10)

        # AI Recommendations Label
        self.ai_recs_label = tk.Label(self.ai_recs_frame,
                                      text="AI Recommendation History:")
        self.ai_recs_label.pack(side=tk.TOP, anchor=tk.W)

        # AI Recommendations Text
        self.ai_recs_text = tk.Text(self.ai_recs_frame, height=10, width=20)
        self.ai_recs_text.pack(side=tk.TOP, anchor=tk.W)

        # AI Aggregate Time Label
        self.ai_agg_time_var = tk.StringVar()
        self.ai_agg_time_var.set(f"Total aggregate time: "
                                 f"{sum(ai_rec[1] 
                            for ai_rec in self.ai_recommendation_history)}s")
        self.ai_agg_time_label = tk.Label(self.ai_recs_frame,
                                      textvariable=self.ai_agg_time_var)
        self.ai_agg_time_label.pack(side=tk.TOP, anchor=tk.W)

        # AI Next Recommendation Label
        self.ai_next_label = tk.Label(self.ai_recs_frame,
                                      text="AI Next Recommendation:")
        self.ai_next_label.pack(side=tk.TOP, anchor=tk.W, pady=(30, 5))

        # AI Next Recommendation Variable Label
        self.ai_next_var = tk.StringVar()
        self.ai_next_var.set("Awaiting AI turn.")
        self.ai_next_label = tk.Label(self.ai_recs_frame,
                                   textvariable=self.ai_next_var)
        self.ai_next_label.pack(side=tk.TOP, anchor=tk.W)

        # Button Frame
        self.button_frame = tk.Frame(self)
        self.button_frame.grid(row=4, column=1, columnspan=2, pady=10)

        # Start Button
        self.start_button = tk.Button(self.button_frame, text="Start",
                                      command=self.start)
        self.start_button.pack(side="left", padx=50)

        # Button Sub frame
        self.button_subframe = tk.Frame(self.button_frame)
        self.button_subframe.pack(side="left", padx=20, pady=20)

        # Input Action Label
        self.input_label = tk.Label(self.button_subframe, text="Input Action:")
        self.input_label.pack(side="left", padx=(20, 0))

        # Action Entry
        self.action_entry = tk.Entry(self.button_subframe, state="disabled")
        self.action_entry.pack(side="left", padx=(0, 20))
        self.action_entry.bind("<Return>",
                               lambda _: self.action_entry_callback())

        # Pause Button
        self.pause_button = tk.Button(self.button_subframe, text="Pause",
                                      command=self.pause,
                                      state="disabled")
        self.pause_button.pack(side="left", padx=5)

        # Resume Button
        self.resume_button = tk.Button(self.button_subframe, text="Resume",
                                       command=self.unpause,
                                       state="disabled")
        self.resume_button.pack(side="left", padx=5)

        # Undo Button
        self.undo_button = tk.Button(self.button_subframe,
                                     text="Undo Last Move",
                                command=self.undo_last_move, state="disabled")
        self.undo_button.pack(side="left", padx=5)

        # Reset Button
        self.reset_button = tk.Button(self.button_subframe, text="Reset",
                                      command=self.reset_game,
                                      state="disabled")
        self.reset_button.pack(side="left", padx=5)

        # Stop Button
        stop_button = tk.Button(self.button_frame, text="Stop",
                            command=lambda: self.controller.display_config())
        stop_button.pack(side="left", padx=50)

    def action_entry_callback(self):
        """Executes the action from the action entry then clears it."""
        action = self.action_entry.get()
        self.action_entry.delete(0, tk.END)
        self.execute_action(action)

    def draw_game_board(self):
        """Draws the game board with the given initial board layout."""
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
                    color_value = 'lightgrey'
                    text_color = 'black'
                    if key in \
                            GameGUI.BOARD_LAYOUTS[self.config['board_layout']][
                                'black']:
                        color_value = 'black'
                        text_color = 'white'
                    elif key in \
                            GameGUI.BOARD_LAYOUTS[self.config['board_layout']][
                                'white']:
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
                    self.canvas.create_text(x, y, text=key, fill=text_color)

    def display_moved_marbles(self, input_action):
        """Updates the positions of marbles then displays it on the screen.

        :param input_action: a string of the old and new pos of the marbles
        """

        source, destination = input_action.split("-")
        source_key_list = []
        for i in range(int(len(source) / 2), 0, -1):
            source_key = source[(i - 1) * 2:2 * i]
            source_key_list.append(source_key)
            destination_key = destination[(i - 1) * 2:2 * i]
            source_color = self.positions[source_key]['color']
            # Update the color of the destination and the source
            self.positions[destination_key]['color'] = source_color
            destination_text_color = 'white' if source_color == 'black' else 'black'
            self.canvas.itemconfig(self.positions[destination_key]['id'],
                                   fill=source_color)
            self.canvas.create_text(self.positions[destination_key]['x'],
                                    self.positions[destination_key]['y'],
                                    text=destination_key,
                                    fill=destination_text_color)
        for source_key in source_key_list:
            if source_key not in destination:
                self.positions[source_key]['color'] = "lightgrey"
                self.canvas.itemconfig(self.positions[source_key]['id'],
                                       fill="lightgrey")
                self.canvas.create_text(self.positions[source_key]['x'],
                                        self.positions[source_key]['y'],
                                        text=source_key,
                                        fill="black")

    def update_display(self):
        """Updates the UI with the changes to the game variables."""
        curr_player = 'human' if self.player_turn == self.config['color_selection'] else 'ai'
        self.turn_var.set(f"Player turn: {self.player_turn.capitalize()} ({curr_player.upper()})")
        self.black_move_var.set(f"Black moves left: {self.num_moves['black']}")
        self.white_move_var.set(f"White moves left: {self.num_moves['white']}")
        self.black_score_label.config(text=f"Black Score: {self.white_loss}")
        self.white_score_label.config(text=f"White Score: {self.black_loss}")

    def display_time(self, *args, owner):
        """A recursive function that decrements the given player's timer.

        :param args: any additional arguments
        :param owner: the player this function was called for
        """
        if self.paused == False and self.player_turn == owner and \
                self.time_left[self.player_turn] > 0:
            self.after(1000, lambda: self.display_time(owner=owner))
            self.time_left[self.player_turn] -= 1
            if self.player_turn == 'black':
                self.black_time_var.set(
                    f"Black time left: {self.time_left['black']}")
            elif self.player_turn == 'white':
                self.white_time_var.set(
                    f"White time left: {self.time_left['white']}")
        elif self.paused == False and self.player_turn == owner and self.time_left[self.player_turn] == 0:
            winner = 'white' if self.player_turn == 'black' else 'black'
            self.reset_game()
            self.state_var.set(f"GAME OVER! {winner.upper()} WINS")

    def start(self):
        """Starts the game as new, resetting the UI then starting a turn."""
        self.state_var.set("PLAYING")
        self.start_button.config(state="disabled")
        self.pause_button.config(state="normal")
        self.reset_button.config(state="disabled")
        self.undo_button.config(state="disabled")
        self.update_display()
        self.start_turn()

    def start_turn(self):
        """Starts a new turn, executing logic based on if human or computer."""
        if self.total_move_number > 0:
            print("starting turn")
            if self.paused is True:
                self.unpause()
            self.display_time(owner=self.player_turn)
            if self.config['color_selection'] != self.player_turn:
                print('Computer turn')
                action = self.actions[self.current_action_index]
                self.current_action_index += 1
                self.ai_next_var.set("Calculating...")
                calculation_time = random.randint(1, 8)
                self.ai_recommendation_history.append(
                    (action, calculation_time))
                self.action_entry.config(state="disabled")
                self.pause_button.config(state="disabled")
                self.resume_button.config(state="disabled")
                self.reset_button.config(state="disabled")
                self.undo_button.config(state="disabled")
                timer = threading.Timer(calculation_time,
                                    lambda: self.ai_next_move_callback(action))
                timer.start()
            else:
                print('Human turn')
                self.action_entry.config(state="normal")

    def ai_next_move_callback(self, action):
        """Updates the AI next recommendation and AI recommendation history."""
        self.ai_next_var.set(f"<{action}>")
        self.update_ai_recommendations()
        self.ai_agg_time_var.set(f"Total aggregate time: {sum(ai_rec[1] 
                            for ai_rec in self.ai_recommendation_history)}")
        self.action_entry.config(state="normal")
        self.pause_button.config(state="normal")

    def update_ai_recommendations(self):
        self.ai_recs_text.delete('1.0', 'end')
        for ai_recommendation in self.ai_recommendation_history:
            self.ai_recs_text.insert(tk.END, f"{ai_recommendation[0]}: {ai_recommendation[1]}s\n")

    def execute_action(self, action):
        """Inputs action by moving marbles, updating log, and ending turn."""
        # Move marbles
        self.display_moved_marbles(action)
        # Update log information with action
        self.log_text.insert(tk.END, f"{self.player_turn.title()}:{action}\n")
        # Complete turn
        self.num_moves[self.player_turn] -= 1
        print("end turn")
        self.ai_next_var.set("Awaiting AI turn.")
        if self.player_turn == 'black':
            self.time_left[self.player_turn] = self.config["black_move_time_limit"]
            self.black_time_var.set(
                f"Black time left: {self.time_left['black']}")
        elif self.player_turn == 'white':
            self.time_left[self.player_turn] = self.config['white_move_time_limit']
            self.white_time_var.set(
                f"White time left: {self.time_left['white']}")
        self.player_turn = "black" if self.player_turn == "white" else "white"
        self.update_display()
        self.start_turn()

    def pause(self):
        """Pauses the game and the timer."""
        self.state_var.set("PAUSED")
        self.action_entry.config(state="disabled")
        self.pause_button.config(state="disabled")
        self.resume_button.config(state="normal")
        self.undo_button.config(state="normal")
        self.reset_button.config(state="normal")
        self.paused = True

    def unpause(self):
        """Unpauses the game and the timer."""
        self.state_var.set("PLAYING")
        self.action_entry.config(state="normal")
        self.pause_button.config(state="normal")
        self.resume_button.config(state="disabled")
        self.undo_button.config(state="disabled")
        self.reset_button.config(state="disabled")
        self.paused = False
        self.display_time(owner=self.player_turn)

    def undo_last_move(self):
        """Undoes the last move from the log."""
        content = self.log_text.get("1.0", tk.END)
        lines = content.split("\n")
        last_log = ""
        last_line_index = 0
        num_lines = len(lines)
        for line in reversed(lines):
            last_line_index += 1
            # Check if the line is not empty
            if line.strip():
                last_log = line.strip()
                break
        a, last_action = last_log.split(":")
        source, destination = last_action.split("-")
        input_action = f"{destination}-{source}"
        self.display_moved_marbles(input_action)
        # Delete the last log from the text widget
        if last_line_index > 0:
            self.log_text.delete(f"end-{last_line_index - 1}l", tk.END)
            self.log_text.insert(tk.END, "\n")
        self.ai_next_var.set("Awaiting AI turn.")
        if (self.config['color_selection'] !=
                self.player_turn or num_lines % 2 == 0):
            self.ai_recommendation_history.pop()
            self.current_action_index -= 1
            self.update_ai_recommendations()
            self.ai_agg_time_var.set(f"Total aggregate time: "
            f"{sum(ai_rec[1] for ai_rec in self.ai_recommendation_history)}s")
        self.player_turn = "black" if self.player_turn == "white" else "white"
        # Reset turns
        self.num_moves[self.player_turn] += 1
        self.update_display()
        self.start_turn()

    def reset_game(self):
        """Clears the board, the log, and the game variables."""
        # Reset
        self.start_button.config(state="normal")
        self.player_turn = 'black'
        self.num_moves = {
            'white': self.config['game_move_limit'],
            'black': self.config['game_move_limit']
        }
        self.time_left = {
            'white': self.config['black_move_time_limit'],
            'black': self.config['white_move_time_limit']
        }
        self.total_move_number = self.config['game_move_limit']
        self.current_action_index = 0
        self.draw_gui()
        self.draw_game_board()
        # Clear log information
        self.log_text.delete(1.0, tk.END)
