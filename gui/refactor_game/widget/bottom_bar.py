import tkinter as tk


class BottomBar(tk.Frame):
    """Contains all the buttons and user input fields."""

    def __init__(self, parent,
                 update_labels_callback,
                 update_board_callback,
                 handle_start_callback,
                 handle_input_confirm_callback,
                 handle_pause_callback,
                 handle_resume_callback,
                 handle_undo_last_move_callback,
                 handle_reset_callback,
                 handle_stop_callback,
                 *args, **kwargs):
        super().__init__(parent, **kwargs)

        self.rowconfigure(0, weight=1)

        self.columnconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)

        # start
        self.start_button = tk.Button(self, text='Start', command=handle_start_callback)
        self.start_button.grid(row=0, column=0)

        # input action
        self.input_action_entry = tk.Entry(self)
        self.input_action_entry.insert(0, 'Enter your action...')
        self.input_action_entry.bind('<FocusIn>', lambda event: self.input_action_entry.delete(0, 'end'))

        def input_confirm(event):
            handle_input_confirm_callback(user_input=self.input_action_entry.get(), update_board_callback=update_board_callback, update_labels_callback=update_labels_callback)
            self.input_action_entry.delete(0, 'end')

        self.input_action_entry.bind('<Return>', lambda event: input_confirm(event))
        self.input_action_entry.grid(row=0, column=1)

        # pause
        self.pause_button = tk.Button(self, text='Pause', command=handle_pause_callback)
        self.pause_button.grid(row=0, column=2)

        # resume
        self.resume_button = tk.Button(self, text='Resume', command=handle_resume_callback)
        self.resume_button.grid(row=0, column=3)

        # undo last move
        self.undo_last_move_button = tk.Button(self, text='Undo Last Move', command=handle_undo_last_move_callback)
        self.undo_last_move_button.grid(row=0, column=4)

        # reset
        self.reset_button = tk.Button(self, text='Reset', command=handle_reset_callback)
        self.reset_button.grid(row=0, column=5)

        # stop
        self.stop_button = tk.Button(self, text='Stop', command=handle_stop_callback)
        self.stop_button.grid(row=0, column=6)
