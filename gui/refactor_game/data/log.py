from statespace.statespace import apply_move


class LogItem():
    def __init__(self, player, move, original_board, result_board, time_taken):
        self.player = player
        self.pre_move_score = player.score
        self.move = move
        self.original_board = original_board
        self.result_board = result_board
        self.time_taken = time_taken

    def __str__(self):
        return f'{self.player.color}:<{self.move}>:({self.time_taken}s)'
