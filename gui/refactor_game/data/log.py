class LogItem():
    def __init__(self, player, move, result_board, time_taken):
        self.player = player
        self.move = move
        self.board = result_board
        self.time_taken = time_taken

    def __str__(self):
        return f'{self.player.color}:<{self.move}>:({self.time_taken}s)'
