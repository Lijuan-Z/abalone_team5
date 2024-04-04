import tkinter as tk
from itertools import zip_longest

from gui.refactor_game.config_page import Operator
from gui.refactor_game.data.player import Player


class SideInfo(tk.Frame):
    """Contains widgets like the p1 log, p2 log, and AI recommendations"""

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent

        self.rowconfigure((0, 1), weight=1)
        self.columnconfigure((0, 1, 2, 3, 4, 5), weight=1)

        self.configure(bg='pink')

        self.combined_log = None

        self.player1_info_frame = None
        self.player2_info_frame = None

    def update_all(self):
        state = self.parent.observed_logical_state
        player1 = state.players[Player.ONE]
        player2 = state.players[Player.TWO]
        self.combined_log.update(player1=player1, player2=player2)
        self.player1_info_frame.update(state.players[Player.ONE])
        self.player2_info_frame.update(state.players[Player.TWO])

    def dynamic_init(self):
        self.combined_log = CombinedLog(self)

        player_1 = self.parent.observed_logical_state.players[Player.ONE]
        player_2 = self.parent.observed_logical_state.players[Player.TWO]

        if player_1.operator == Operator.HUMAN.value:
            self.player1_info_frame = HumanInfo(self)
        elif player_1.operator == Operator.AI.value:
            self.player1_info_frame = AIInfo(self)
        else:
            raise ValueError(f"invalid operator: {player_1.operator}")

        if player_2.operator == Operator.HUMAN.value:
            self.player2_info_frame = HumanInfo(self)
        elif player_2.operator == Operator.AI.value:
            self.player2_info_frame = AIInfo(self)
        else:
            raise ValueError(f"invalid operator: {player_2.operator}")

        self.combined_log.grid(row=0, column=0, columnspan=6, padx=(0, 50),
                               pady=(0, 0), sticky='nsew')
        self.player1_info_frame.grid(row=1, column=0, columnspan=3,
                                     padx=(0, 5), pady=(0, 10), sticky='nsew')
        self.player2_info_frame.grid(row=1, column=3, columnspan=3,
                                     padx=(5, 50), pady=(0, 10), sticky='nsew')


class CombinedLog(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, **kwargs)

        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        self.log_entry = tk.Text(self, width=10, height=10, bg='purple')

        self.frame_title = tk.Label(self.log_entry, text="Combined Move Log",
                                    relief=tk.FLAT)
        self.frame_title.grid(row=0, column=0, sticky='nw')

        self.log_entry.grid(row=1, column=0, rowspan=1, columnspan=1,
                            sticky='nsew')

    def update(self, player1, player2):
        self.log_entry.delete('1.0', tk.END)
        self.log_entry.insert(tk.END, "\n\n")
        for log1, log2 in zip_longest(player1.log, player2.log):
            if log1 is not None:
                self.log_entry.insert(tk.END, f"{str(log1)}\n")
            if log2 is not None:
                self.log_entry.insert(tk.END, f"{str(log2)}\n")
        self.log_entry.see(tk.END)



class HumanInfo(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent

        self.configure(bg='purple')

        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        self.log_entry = tk.Text(self, width=10, height=10, bg='purple')
        self.log_entry.insert(tk.END, "Human")
        self.log_entry.grid(row=1, column=0, rowspan=1, columnspan=1,
                            pady=(10, 0), sticky='nsew')

        self.frame_title = tk.Label(self.log_entry, text="Player1 Move Log",
                                    relief=tk.FLAT)
        self.frame_title.grid(row=0, column=0, sticky='nw')

    def update(self, player):
        self.log_entry.delete('1.0', tk.END)
        self.log_entry.insert(tk.END, "\n\n")
        for log in player.log:
            self.log_entry.insert(tk.END, f"{str(log)}\n")
        self.log_entry.see(tk.END)

        self.log_entry.insert(tk.END, f"\n\nTotal Aggregate Time: {sum([log_item.time_taken for log_item in player.log])}s")


class AIInfo(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent

        self.configure(bg='cyan')

        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=10)
        self.rowconfigure(2, weight=1)

        self.columnconfigure(0, weight=1)

        self.log_entry = tk.Text(self, width=10, height=10, bg='red')
        self.log_entry.insert(tk.END, "AI")
        self.log_entry.grid(row=1, column=0, rowspan=1, columnspan=1,
                            pady=(10, 10), sticky='nsew')

        self.frame_title = tk.Label(self.log_entry,
                                    text="Player2 AI Recommendation History",
                                    relief=tk.FLAT)
        self.frame_title.grid(row=0, column=0, sticky='nw')

        self.ai_recommendation_log = tk.Text(self, width=10, height=10)
        self.ai_recommendation_log.insert(tk.END, "current recommendation")

        self.ai_recommendation_log.grid(row=2, column=0, rowspan=1,
                                        columnspan=1, sticky='nsew')

    def update(self, player):
        self.log_entry.delete('1.0', tk.END)
        self.log_entry.insert(tk.END, "\n\n")
        for log in player._recommendation_history:
            self.log_entry.insert(tk.END, f"{str(log)}\n")

        self.log_entry.insert(tk.END, f"\n\nTotal Aggregate Time: {sum([log.time_taken for log in player._recommendation_history])}s")


        self.log_entry.see(tk.END)
