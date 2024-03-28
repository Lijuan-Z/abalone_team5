"""Functions for marble coordinates."""
valid_coords = {11, 12, 13, 14, 15, 21, 22, 23, 24, 25, 26, 31, 32, 33, 34, 35, 36, 37, 41, 42, 43, 44, 45, 46, 47, 48, 51, 52, 53, 54, 55, 56, 57, 58, 59, 62, 63, 64, 65, 66, 67, 68, 69, 73, 74, 75, 76, 77, 78, 79, 84, 85, 86, 87, 88, 89, 95, 96, 97, 98, 99}

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
    # row = marble_coord // 10
    # col = marble_coord % 10
    return marble_coord not in valid_coords
