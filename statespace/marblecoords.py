"""Functions for marble coordinates."""

BOUNDS = {
    0: (5, 4),
    1: (1, 5),
    2: (1, 6),
    3: (1, 7),
    4: (1, 8),
    5: (1, 9),
    6: (2, 9),
    7: (3, 9),
    8: (4, 9),
    9: (5, 9),
    10: (5, 4),
    11: (5, 4)
}


def is_out_of_bounds(marble_coord: int) -> bool:
    """True if marble coord is out of bounds of an abalone board."""
    row = marble_coord // 10
    col = marble_coord % 10
    return col < BOUNDS[row][0] or col > BOUNDS[row][1]
