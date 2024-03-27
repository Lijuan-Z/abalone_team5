"""This module holds the Game GUI."""
import math
import random
import threading
import tkinter as tk


class SimulationGUI(tk.Frame):
    """SimulationGUI displays the game board and executes game logic."""

    SESSION_ID = 0
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
    AI_HARDCODED_ACTIONS = {
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
        """Initializes a new SimulationGUI and starts the game.

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
            SimulationGUI.DEFAULT_CONFIG)
        print(self.config)

        # Game info
        SimulationGUI.SESSION_ID += 1
        self.positions = {}
        self.player_turn = 'black'
        self.paused = False
        self.num_moves = {
            'white': self.config['game_move_limit'],
            'black': self.config['game_move_limit']
        }
        self.time_left = {
            'white': self.config['white_move_time_limit'],
            'black': self.config['black_move_time_limit']
        }
        self.total_move_number = self.config['game_move_limit']

        # hard code AI moves: only for test purpose
        player_color = self.config['color_selection']
        ai_color = 'black' if player_color == 'white' else 'white'
        self.actions = self.AI_HARDCODED_ACTIONS[self.config['board_layout']][
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



    def action_entry_callback(self):
        """Executes the action from the action entry then clears it."""
        action = self.action_entry.get()
        self.action_entry.delete(0, tk.END)
        self.execute_action(action)

    def draw_game_board(self):
        """Draws the game board with the given initial board layout."""
        r = SimulationGUI.CIRCLE_RADIUS
        cols = SimulationGUI.COLUMNS
        for i in range(9):
            for j in range(-4, 5):
                if abs(j) >= i or i < 9 - abs(j):
                    x = 40 + (2 * i + 1) * r + abs(j) * r
                    y = 300 - r * j * math.sqrt(3)
                    k = j if j > 0 else 0
                    key = f'{cols[j + 4]}{i + 1 + k}'
                    # Set the values for x0, x1, y0, y1, and color for each key
                    color_value = 'lightgrey'
                    text_color = 'black'
                    if key in \
                            SimulationGUI.BOARD_LAYOUTS[self.config['board_layout']][
                                'black']:
                        color_value = 'black'
                        text_color = 'white'
                    elif key in \
                            SimulationGUI.BOARD_LAYOUTS[self.config['board_layout']][
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
            destination_text_color = 'white' \
                if source_color == 'black' else 'black'
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
        curr_player = 'human' \
            if self.player_turn == self.config['color_selection'] else 'ai'
        self.turn_var.set(f"Player turn: {self.player_turn.capitalize()} "
                          f"({curr_player.upper()})")
        self.black_move_var.set(f"Black moves left: {self.num_moves['black']}")
        self.white_move_var.set(f"White moves left: {self.num_moves['white']}")
        self.black_score_label.config(text=f"Black Score: {self.white_loss}")
        self.white_score_label.config(text=f"White Score: {self.black_loss}")

    def display_time(self, *args, owner, session_id):
        """A recursive function that decrements the given player's timer.

        :param args: any additional arguments
        :param owner: the player this function was called for
        """
        print("current session: ", SimulationGUI.SESSION_ID)
        print("timer's session: ", session_id)
        print("")
        if (self.paused is False and self.player_turn == owner and
                self.time_left[self.player_turn] > 0 and
                SimulationGUI.SESSION_ID == session_id):
            self.after(1000, lambda: self.display_time(owner=owner,
                                                       session_id=session_id))
            self.time_left[self.player_turn] -= 1
            if self.player_turn == 'black':
                self.black_time_var.set(
                    f"Black time left: {self.time_left['black']}")
            elif self.player_turn == 'white':
                self.white_time_var.set(
                    f"White time left: {self.time_left['white']}")
        elif ((self.paused is False and self.player_turn == owner and
              self.time_left[self.player_turn] == 0) and
              SimulationGUI.SESSION_ID == session_id):
            print('reached')
            self.reset_game()

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
            self.display_time(owner=self.player_turn,
                              session_id=SimulationGUI.SESSION_ID)
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
                                        lambda: self.ai_next_move_callback(
                                            action))
                timer.start()
            else:
                print('Human turn')
                self.action_entry.config(state="normal")

    def ai_next_move_callback(self, action):
        """Updates the AI next recommendation and AI recommendation history."""
        self.ai_next_var.set(f"<{action}>")
        self.update_ai_recommendations()
        total_aggregate_time = (
            sum(ai_rec[1] for ai_rec in self.ai_recommendation_history))
        self.ai_agg_time_var.set(f"Total aggregate time: "
                                 f"{total_aggregate_time}")
        self.action_entry.config(state="normal")
        self.pause_button.config(state="normal")

    def update_ai_recommendations(self):
        self.ai_recs_text.delete('1.0', 'end')
        for ai_recommendation in self.ai_recommendation_history:
            self.ai_recs_text.insert(tk.END, f"{ai_recommendation[0]}: "
                                             f"{ai_recommendation[1]}s\n")

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
            self.time_left[self.player_turn] = self.config[
                "black_move_time_limit"]
            self.black_time_var.set(
                f"Black time left: {self.time_left['black']}")
        elif self.player_turn == 'white':
            self.time_left[self.player_turn] = self.config[
                'white_move_time_limit']
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
        self.display_time(owner=self.player_turn,
                          session_id=SimulationGUI.SESSION_ID)

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
            total_aggregate_time = sum(ai_rec[1] for ai_rec in
                                       self.ai_recommendation_history)
            self.ai_agg_time_var.set(f"Total aggregate time: "
                                     f"{total_aggregate_time}s")
        self.player_turn = "black" if self.player_turn == "white" else "white"
        # Reset turns
        self.num_moves[self.player_turn] += 1
        self.update_display()
        self.start_turn()

    def reset_game(self):
        """Transitions to a fresh SimulationGUI."""
        self.controller.display_game(self.config)