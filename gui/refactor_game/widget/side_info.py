import tkinter as tk

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

        self.combined_log.grid(row=0, column=0, columnspan=6, padx=(0, 50), pady=(0,0), sticky='nsew')
        self.player1_info_frame.grid(row=1, column=0, columnspan=3, padx=(0, 5), pady=(0, 10), sticky='nsew')
        self.player2_info_frame.grid(row=1, column=3, columnspan=3, padx=(5, 50), pady=(0, 10), sticky='nsew')

class CombinedLog(tk.Frame):

     def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, **kwargs)

        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)


        self.log_entry = tk.Text(self, width=10, height=10, bg='purple')

        self.frame_title = tk.Label(self.log_entry, text="Combined Move Log", relief=tk.FLAT)
        self.frame_title.grid(row=0, column=0, sticky='nw')

        self.log_entry.grid(row=1, column=0, rowspan=1, columnspan=1, sticky='nsew')


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
        self.log_entry.grid(row=1, column=0, rowspan=1, columnspan=1, pady=(10, 0), sticky='nsew')

        self.frame_title = tk.Label(self.log_entry, text="Player1 Move Log", relief=tk.FLAT)
        self.frame_title.grid(row=0, column=0, sticky='nw')



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
        self.log_entry.grid(row=1, column=0, rowspan=1, columnspan=1, pady=(10, 10), sticky='nsew')

        self.frame_title = tk.Label(self.log_entry, text="Player2 AI Recommendation History", relief=tk.FLAT)
        self.frame_title.grid(row=0, column=0, sticky='nw')



        self.ai_recommendation_log = tk.Text(self, width=10, height=10)
        self.ai_recommendation_log.insert(tk.END, "current recommendation")

        self.ai_recommendation_log.grid(row=2, column=0, rowspan=1, columnspan=1, sticky='nsew')
