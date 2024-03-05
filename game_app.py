import tkinter as tk
from main_page import GameGUI
from config_page import ConfigGUI


class GameApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        board_frame = tk.Frame(self, width=400, height=400, bg="white")
        board_frame.grid(row=0, column=1, rowspan=3)

        self.frames = {}
        for F in (ConfigGUI, GameGUI):
            frame = F(board_frame, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(ConfigGUI)

    def show_frame(self, gui):
        frame = self.frames[gui]
        frame.tkraise()


app = GameApp()
app.mainloop()
