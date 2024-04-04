import tkinter as tk


class BottomBar(tk.Frame):
    """Contains all the buttons and user input fields."""

    def __init__(self, parent,
                 *args, **kwargs):
        super().__init__(parent, **kwargs)

        self.parent = parent

        self.rowconfigure(0, weight=1)

        self.columnconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)

        # start
        self.start_button = tk.Button(self, text='Start', command=self.parent.observed_logical_state.handle_start_callback)
        self.start_button.grid(row=0, column=0)

        # input action
        self.input_action_entry = tk.Entry(self)
        self.input_action_entry.insert(0, 'Enter your action...')
        self.input_action_entry.bind('<FocusIn>', lambda _: self.input_action_entry.delete(0, 'end'))

        def input_confirm():
            entry_action = self.input_action_entry.get()
            self.parent.observed_logical_state.handle_input_confirm_callback(user_input=entry_action)
            self.input_action_entry.delete(0, 'end')

        self.input_action_entry.bind('<Return>', lambda _: input_confirm())
        self.input_action_entry.grid(row=0, column=1)

        # pause
        self.pause_button = tk.Button(self, text='Pause', command=self.parent.observed_logical_state.handle_pause_callback)
        self.pause_button.grid(row=0, column=2)

        # resume
        self.resume_button = tk.Button(self, text='Resume', command=self.parent.observed_logical_state.handle_resume_callback)
        self.resume_button.grid(row=0, column=3)

        # undo last move
        self.undo_last_move_button = tk.Button(self, text='Undo Last Move', command=self.parent.observed_logical_state.handle_undo_last_move_callback)
        self.undo_last_move_button.grid(row=0, column=4)

        # reset
        self.reset_button = tk.Button(self, text='Reset', command=self.parent.observed_logical_state.handle_reset_callback)
        self.reset_button.grid(row=0, column=5)

        # stop
        self.stop_button = tk.Button(self, text='Stop', command=self.parent.observed_logical_state.handle_stop_callback)
        self.stop_button.grid(row=0, column=6)
