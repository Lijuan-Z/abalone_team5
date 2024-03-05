import math
import tkinter as tk
from tkinter import ttk

#temp
LARGEFONT = ("Verdana", 35)


class GameApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # Game Board Frame
        board_frame = tk.Frame(self, width=400, height=400, bg="white")
        board_frame.grid(row=0, column=1, rowspan=3)

        self.frames = {}
        for F in (ConfigGUI, TestGUI):
            frame = F(board_frame, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(ConfigGUI)

    def show_frame(self, gui):
        frame = self.frames[gui]
        frame.tkraise()


class ConfigGUI(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # label of frame Layout 2
        label = ttk.Label(self, text="Config page", font=LARGEFONT)

        # putting the grid in its place by using
        # grid
        label.grid(row=0, column=4, padx=10, pady=10)

        button1 = ttk.Button(self, text="Page 1",
                             command=lambda: controller.show_frame(TestGUI))

        # putting the button in its place by
        # using grid
        button1.grid(row=1, column=1, padx=10, pady=10)


class TestGUI(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # label of frame Layout 2
        label = ttk.Label(self, text="test gui")

        # putting the grid in its place by using
        # grid
        label.grid(row=0, column=4, padx=10, pady=10)

        button1 = ttk.Button(self, text="Page 1",
                             command=lambda: controller.show_frame(ConfigGUI))

        # putting the button in its place by
        # using grid
        button1.grid(row=1, column=1, padx=10, pady=10)


class GameGUI:
    def __init__(self, master, controller):
        self.master = master
        master.title("Abalone")

        # Draw circles based on configuration
        # todo: pass configurations
        # Initialize an empty dictionary
        self.positions = {}
        self.draw_game_board()

        # Log Information Frame
        self.log_frame = tk.Frame(master, width=100, height=400, bg="lightgrey")
        self.log_frame.grid(row=0, column=2, rowspan=3)

        # Log Label
        self.log_label = tk.Label(self.log_frame, text="Logs")
        self.log_label.pack()

        # Log Information Text
        self.log_text = tk.Text(self.log_frame, height=10, width=20)
        self.log_text.pack()

        # Button Frame
        self.button_frame = tk.Frame(master)
        self.button_frame.grid(row=3, column=1, columnspan=2, pady=10)

        # Reset Button
        self.reset_button = tk.Button(self.button_frame, text="Reset",
                                      command=self.reset_game)
        self.reset_button.grid(row=0, column=0, padx=5)

        # Undo Button
        self.undo_button = tk.Button(self.button_frame, text="Undo Last Move",
                                     command=self.undo_last_move)
        self.undo_button.grid(row=0, column=1, padx=5)

        # Input Action Label
        self.input_label = tk.Label(self.button_frame, text="Input Action:")
        self.input_label.grid(row=1, column=0, padx=5)

        # Action Entry
        self.action_entry = tk.Entry(self.button_frame)
        self.action_entry.grid(row=1, column=1, padx=5)
        self.action_entry.bind("<Return>", self.set_action)

        # Configuration Label
        self.config_label = tk.Label(master, text="Move Limit:")
        self.config_label.grid(row=0, column=0)

        # Configuration Entry
        self.config_entry = tk.Entry(master)
        self.config_entry.grid(row=1, column=0, pady=10)

        # Dropdown Label
        self.config_label = tk.Label(master, text="Layout Selection:")
        self.config_label.grid(row=2, column=0)

        # Dropdown Options
        self.options = ['Standard', 'German daisy', 'Belgian daisy']

        # Dropdown
        self.dropdown_var = tk.StringVar(master)
        self.dropdown_var.set(self.options[0])
        self.dropdown_menu = ttk.Combobox(master,
                                          textvariable=self.dropdown_var,
                                          values=self.options)
        self.dropdown_menu.grid(row=3, column=0)

        # Start Button
        self.start_button = tk.Button(master, text="Start", command=self.start)
        self.start_button.grid(row=4, column=0, pady=5)

    def reset_game(self):
        # Reset

        # Clear log information
        self.log_text.delete(1.0, tk.END)

    def undo_last_move(self):
        print("undo_last_move")
        # Update log information
        # self.log_text.insert(tk.END, "Undo?\n")

    def set_action(self, event):
        # Set the action on user input
        input_action = self.action_entry.get()
        source, destination = input_action.split("-")

        color = self.positions[source]['color']
        # Update the color of the destination and the source
        self.positions[destination]['color'] = color
        self.positions[source]['color'] = "lightgrey"

        # Update the color of the circle on the canvas
        self.canvas.itemconfig(self.positions[source]['id'], fill="lightgrey")
        self.canvas.itemconfig(self.positions[destination]['id'], fill=color)

        # Update log information with action entered by the user
        self.log_text.insert(tk.END, f"Action: {input_action}\n")

    def draw_game_board(self):
        r = 30
        cols = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
        for i in range(9):
            for j in range(-4, 5):
                if (abs(j) >= i or i < 9 - abs(j)):
                    x = 40 + (2 * i + 1) * r + abs(j) * r
                    y = 300 - r * j * math.sqrt(3)
                    key = f'{cols[j + 4]}{i + 1}'  # Construct the key string
                    # Set the values for x0, x1, y0, y1, and color for each key
                    color_value = "lightgrey"
                    if cols[j + 4] == 'a' or cols[
                        j + 4] == 'b' or key == 'c3' or key == 'c4' or key == 'c5':
                        color_value = 'black'
                    if cols[j + 4] == 'h' or cols[
                        j + 4] == 'i' or key == 'g3' or key == 'g4' or key == 'g5':
                        color_value = 'white'
                    self.positions[key] = {
                        'x0': x - r,
                        'x1': x + r,
                        'y0': y - r,
                        'y1': y + r,
                        'color': color_value
                    }
                    # self.canvas.create_text(x, y, text=key)

        for key in self.positions:
            x0, y0 = self.positions[key]['x0'], self.positions[key]['y0']
            x1, y1 = self.positions[key]['x1'], self.positions[key]['y1']
            self.positions[key]['id'] = self.canvas.create_oval(x0, y0, x1, y1,
                                                                fill=
                                                                self.positions[
                                                                    key][
                                                                    'color'])

    def start(self):
        try:
            move_limit = int(self.config_entry.get())
            if move_limit > 0:
                self.draw_game_board()
            else:
                raise ValueError("Number of move must be positive")
        except ValueError:
            self.log_text.insert(tk.END, "Invalid input for number of move!\n")

        selected_option = self.dropdown_var.get()
        # self.log_text.insert(tk.END, f"Selected option: {selected_option}\n")
        print(f"Selected option: {selected_option}\n")


# root = tk.Tk()
# game_gui = GameGUI(root)
# root.mainloop()

app = GameApp()
app.mainloop()
