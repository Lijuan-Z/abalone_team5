import tkinter as tk

from gui.refactor_game.data.player import Player


class TopInfo(tk.Frame):
    """Contains information like score, turns remaining, etc."""

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.columnconfigure(0, weight=4)
        self.columnconfigure((1, 2, 3, 4, 5), weight=1)
        self.columnconfigure(6, weight=4)

        self.player_time_left_stringvar = {}
        self.player_time_left_stringvar[Player.ONE] = tk.StringVar()
        self.player_time_left_stringvar[Player.ONE].set("")

        self.player_time_left_stringvar[Player.TWO] = tk.StringVar()
        self.player_time_left_stringvar[Player.TWO].set("")

        self.cur_player_label = tk.Label(self, text="")
        self.game_state_label = tk.Label(self, text="")
        self.player_1_marble_color_label = tk.Label(self, text="")
        self.player_1_turns_left_label = tk.Label(self, text="")
        self.player_1_score_label = tk.Label(self, text="")
        self.player_1_time_left_label = tk.Label(self, textvariable=self.player_time_left_stringvar[Player.ONE])
        self.player_2_marble_color_label = tk.Label(self, text="")
        self.player_2_turns_left_label = tk.Label(self, text="")
        self.player_2_score_label = tk.Label(self, text="")
        self.player_2_time_left_label = tk.Label(self, textvariable=self.player_time_left_stringvar[Player.TWO])

        self.cur_player_label.grid(row=0, column=1)
        self.game_state_label.grid(row=1, column=1)
        self.player_1_marble_color_label.grid(row=0, column=2)
        self.player_1_turns_left_label.grid(row=0, column=3)
        self.player_1_score_label.grid(row=0, column=4)
        self.player_1_time_left_label.grid(row=0, column=5)
        self.player_2_marble_color_label.grid(row=1, column=2)
        self.player_2_turns_left_label.grid(row=1, column=3)
        self.player_2_score_label.grid(row=1, column=4)
        self.player_2_time_left_label.grid(row=1, column=5)

    def update_labels(self):
        info = self.parent.observed_logical_state.get_top_info()
        self.set_labels(**info)

    def set_labels(self,
                   game_state,
                   cur_player,
                   player_1_marble_color,
                   player_1_turns_left,
                   player_1_score,
                   player_1_time_left,
                   player_1_operator,
                   player_2_marble_color,
                   player_2_turns_left,
                   player_2_score,
                   player_2_time_left,
                   player_2_operator,
                   **kwargs):
        self.game_state_label.config(text=f'game state: {game_state}')
        self.cur_player_label.config(text=f'cur player: {cur_player}')
        self.player_1_marble_color_label.config(
            text=f'Player1: {player_1_operator}-{player_1_marble_color}')
        self.player_1_turns_left_label.config(
            text=f'Player1 Turn Left: {player_1_turns_left}')
        self.player_1_score_label.config(
            text=f'Player1 Score: {player_1_score}')
        # self.player_1_time_left_label.config(
        #     text=f'Player1 Time Left: {player_1_time_left}')
        self.player_time_left_stringvar[Player.ONE].set(f'Player1 Time Left: {round(player_1_time_left / 100, 2):0.2f}')
        self.player_2_marble_color_label.config(
            text=f'Player2: {player_2_operator}-{player_2_marble_color}')
        self.player_2_turns_left_label.config(
            text=f'Player2 Turns Left: {player_2_turns_left}')
        self.player_2_score_label.config(
            text=f'Player2 Score: {player_2_score}')
        # self.player_2_time_left_label.config(
        #     text=f'Player2 Time_left: {player_2_time_left}')
        self.player_time_left_stringvar[Player.TWO].set(f'Player2 Time_left: {round(player_2_time_left / 100, 2):0.2f}')
