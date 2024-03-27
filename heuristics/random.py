"""Contains a heuristic that returns random values."""
import random


def eval_state(*args, **kwargs):
    """Returns a random evaluation result."""
    return random.randint(0, 100)
