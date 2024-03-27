"""Currently a testing file for the best-move search algorithm."""
from statespace import external
from statespace import statespace

in_base = "tests/in/"
out_base = "tests/out/"


test_num = 2
board_marbles, player_color = external.in_to_marbles(f"{in_base}Test{test_num}.input")
statespace.iterative_deepening_alpha_beta_search(board_marbles, 0, 10000, 15)
