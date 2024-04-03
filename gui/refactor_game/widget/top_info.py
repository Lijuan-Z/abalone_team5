import tkinter as tk


class TopInfo(tk.Frame):
    """Contains information like score, turns remaining, etc."""

    def __init__(self, parent, get_top_info_callback, *args, **kwargs):
        super().__init__(parent, **kwargs)
        self.get_top_info_callback = get_top_info_callback

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.columnconfigure(0, weight=4)
        self.columnconfigure((1, 2, 3, 4, 5), weight=1)
        self.columnconfigure(6, weight=4)

        self.game_state_label = tk.Label(self, text="")
        self.cur_player_label = tk.Label(self, text="")
        self.player_1_marble_color_label = tk.Label(self, text="")
        self.player_1_turns_left_label = tk.Label(self, text="")
        self.player_1_score_label = tk.Label(self, text="")
        self.player_1_time_left_label = tk.Label(self, text="")
        self.player_2_marble_color_label = tk.Label(self, text="")
        self.player_2_turns_left_label = tk.Label(self, text="")
        self.player_2_score_label = tk.Label(self, text="")
        self.player_2_time_left_label = tk.Label(self, text="")

        self.game_state_label.grid(row=0, column=1)
        self.cur_player_label.grid(row=1, column=1)
        self.player_1_marble_color_label.grid(row=0, column=2)
        self.player_1_turns_left_label.grid(row=0, column=3)
        self.player_1_score_label.grid(row=0, column=4)
        self.player_1_time_left_label.grid(row=0, column=5)
        self.player_2_marble_color_label.grid(row=1, column=2)
        self.player_2_turns_left_label.grid(row=1, column=3)
        self.player_2_score_label.grid(row=1, column=4)
        self.player_2_time_left_label.grid(row=1, column=5)

        self.update_labels()

    def update_labels(self):
        info = self.get_top_info_callback()
        self.set_labels(**info)

    def set_labels(self,
                   game_state,
                   cur_player,
                   player_1_marble_color,
                   player_1_turns_left,
                   player_1_score,
                   player_1_time_left,
                   player_2_marble_color,
                   player_2_turns_left,
                   player_2_score,
                   player_2_time_left,
                   **kwargs):
        self.game_state_label.config(text=f'game state: {game_state}')
        self.cur_player_label.config(text=f'cur player: {cur_player}')
        self.player_1_marble_color_label.config(
            text=f'player 1 marble_color: {player_1_marble_color}')
        self.player_1_turns_left_label.config(
            text=f'player 1 turns_left: {player_1_turns_left}')
        self.player_1_score_label.config(
            text=f'player 1 score: {player_1_score}')
        self.player_1_time_left_label.config(
            text=f'player 1 time_left: {player_1_time_left}')
        self.player_2_marble_color_label.config(
            text=f'player 2 marble_color: {player_2_marble_color}')
        self.player_2_turns_left_label.config(
            text=f'player 2 turns_left: {player_2_turns_left}')
        self.player_2_score_label.config(
            text=f'player 2 score: {player_2_score}')
        self.player_2_time_left_label.config(
            text=f'player 2 time_left: {player_2_time_left}')
