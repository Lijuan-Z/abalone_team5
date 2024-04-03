import math
import tkinter as tk

class Board(tk.Frame):
    """Displays the game board."""
    CIRCLE_RADIUS = 30
    COLUMNS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']

    def __init__(self, parent,
                 get_board_callback,
                 *args, **kwargs):
        super().__init__(parent, **kwargs)
        self.canvas = tk.Canvas(self, bg="pink")
        self.canvas.bind("<Button-1>", lambda event: print(f'{event.x}:{event.y}'))

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.canvas.grid(row=0, column=0, sticky='nsew')
        self.bind("<Configure>",
                  lambda event: self.update_board(
                      get_board_callback()
                  ))

    def click_coord_to_marble_coord(self, coord):
        pass

    def update_board(self, board: dict[int, int]):
        """Updates the canvas to draw the given board."""
        self.update()

        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        r = 0.03 * math.sqrt((canvas_width ** 2) + (canvas_height ** 2))

        board_length = r * 18

        x_offset = (canvas_width / 2) - (board_length / 2)
        y_offset = (canvas_height / 2)

        self.canvas.delete('all')
        for col in range(9):
            for row in range(-4, 5):
                if abs(row) >= col or col < 9 - abs(row):
                    x = x_offset + (2 * col + 1) * r + abs(row) * r
                    y = y_offset - r * row * math.sqrt(3)

                    color_value = '#7E7E7E'
                    text_color = 'black'

                    k = row if row > 0 else 0

                    key = f'{self.COLUMNS[row + 4]}{col + 1 + k}'

                    self.canvas.create_oval(
                        x - r, y - r, x + r, y + r,
                        fill=color_value
                    )

                    self.canvas.create_text(x, y, text=key,
                                            fill=text_color)

                    self.update()

        # print(board.items())
        offsets = [0, 0, 0, 0, 0, 0, 1, 2, 3, 4]
        for coord, color in board.items():
            # row = (coord)-5) // 10
            # col = (coord - 1 - (coord//10)) % 10

            row = ((coord//10) - 5)
            col = ((coord%10) - 1 - offsets[(coord//10)])

            x = x_offset + (2 * col + 1) * r + abs(row) * r
            y = y_offset - r * row * math.sqrt(3)

            color_value = 'black' if color == 0 else 'white'
            text_color = 'white' if color == 0 else 'black'

            self.canvas.create_oval(
                x - r, y - r, x + r, y + r,
                fill=color_value
            )

            k = row if row > 0 else 0
            key = f'{self.COLUMNS[row + 4]}{col + 1 + k}'
            self.canvas.create_text(x, y, text=key,
                                    fill=text_color)
            self.update()
