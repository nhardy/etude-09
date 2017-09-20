#!/usr/bin/env python3

"""
Etude 9 - Sir Tet's Carpets
Authors: Daniel Thomson, Levi Faid, Nathan Hardy, Rebecca Wilson
"""

import sys
from typing import Tuple

class Grid:
    """
    Abstraction useful for serialising Grid state
    """

    def __init__(self, width: int, length: int):
        self.width = width
        self.length = length

        self._grid = [[False for _ in range(length)] for _ in range(width)]

    def fill(self, coords: Tuple[int, int]):
        """
        Sets the Grid cell at (x, y) as filled
        """

        x_pos, y_pos = coords
        self._grid[x_pos][y_pos] = True

    def serialise(self) -> int:
        """
        Returns a unique integer representing the state of Grid
        """

        total = 0

        for i, row in enumerate(self._grid):
            for j, cell in enumerate(row):
                if cell:
                    total += i * self.width + j

        return total

def result(width: int, length: int) -> int:
    """
    Returns the number of combinations of carpets possible for
    a carpet of dimensions (width * length)
    """

    # Areas not divisible by 4 are impossible to fill
    if width * length % 4 != 0:
        return 0

    # Dictionary of "Grid state" -> "No. of Combinations"
    # This will be progressively built up by a depth-first search tree
    # where if a given "Grid state" has already been reached, one
    # can simply add the "No. of Combinations" instead of traversing
    # further, if that value had already been calculated.
    grid_states = {}

    # TODO: Depth-First Search here

    # The Final result will be stored in the empty Grid state
    return grid_states[Grid(width, length).serialise()]

def main():
    """
    Interprets input according to specifications and produces the result
    according to the output format defined by the etude
    """

    for unstripped_line in sys.stdin.readlines():
        line = unstripped_line.strip()

        if line.startswith('#') or line == '':
            continue

        width, length = map(int, line.split())

        print(line)
        print('# {}'.format(result(width, length)))

if __name__ == '__main__':
    main()
