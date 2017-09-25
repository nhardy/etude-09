#!/usr/bin/env python3

"""
Etude 9 - Sir Tet's Carpets
Authors: Daniel Thomson, Levi Faid, Nathan Hardy, Rebecca Wilson
"""

import sys
from typing import List, Optional, Tuple, Type


class Piece:
    """
    Abstraction useful for modeling Pieces
    """

    @staticmethod
    def rotate(locations: Tuple[Tuple[bool, ...], ...]) -> Tuple[Tuple[bool, ...], ...]:
        """
        Helper method for rotating a 2D array one turn clockwise
        @see https://stackoverflow.com/questions/8421337/rotating-a-two-dimensional-array-in-python
        """

        return tuple(zip(*locations[::-1]))

    @classmethod
    def get_all(cls: 'Piece') -> List[Type['Piece']]:
        """
        Returns a list of all Pieces
        """

        return [
            # 2x2
            cls(((True, True,), (True, True,),), 1),
            # 1x4
            cls(((True, True, True, True,),), 2),
            # s
            cls(((False, True, True,), (True, True, False,),), 4),
            # z
            cls(((True, True, False,), (False, True, True,),), 4),
            # L
            cls(((True, True, True,), (True, False, False,),), 4),
            # J
            cls(((True, False, False,), (True, True, True,),), 4),
            # T
            cls(((True, True, True,), (False, True, False,),), 4),
        ]

    @classmethod
    def get_all_piece_rotations(cls: 'Piece') -> List[Type['Piece']]:
        """
        Returns a list of all Pieces and their unique rotations
        """

        return [r for p in cls.get_all() for r in p.get_rotations()]

    def __init__(self, locations: Tuple[Tuple[bool]], rotations: int):
        self.locations = locations
        self._rotations = rotations

    def get_rotations(self) -> List['Piece']:
        """
        Returns all the rotations for the current Piece
        """

        rotations = [self]
        tmp = self

        for _ in range(self._rotations - 1):
            tmp = Piece(Piece.rotate(tmp.locations), self._rotations)
            rotations.append(tmp)

        return rotations

class Grid:
    """
    Abstraction useful for dealing with Grid state.
    It is important to note that all properties are immuntable.
    """

    def __init__(self, width: int, length: int, cells: Tuple[Tuple[bool, ...], ...]=None):
        self._width = width
        self._length = length

        # We're specifically using a tuple of tuples here to
        # enforce immutability
        self._cells = cells if cells is not None else tuple(
            tuple(False for _ in range(length)) for _ in range(width)
        )

    @property
    def width(self):
        return self._width

    @property
    def length(self):
        return self._length

    def place(self, piece: Piece, coords: Tuple[int, int]) -> Optional['Grid']:
        """
        Tries to place the piece at position (x, y).
        If this fails, returns None.
        """

        x_pos, y_pos = coords
        piece_locations = piece.locations

        if len(piece_locations) + y_pos > self._width:
            return None
        if len(piece_locations[0]) + x_pos > self._length:
            return None

        changes = set()

        for p_y_pos, row in enumerate(piece_locations):
            for p_x_pos, cell in enumerate(row):
                if cell:
                    cell_y_pos = y_pos + p_y_pos
                    cell_x_pos = x_pos + p_x_pos

                    # If both the cell of the piece and the cell of the
                    # Grid are filled, we cannot procede
                    if self._cells[cell_y_pos][cell_x_pos]:
                        return None

                    changes.add((cell_x_pos, cell_y_pos))

        return Grid(self._width, self._length, tuple(
            tuple(
                cell or (False if (cell_x_pos, cell_y_pos) not in changes else True) for cell_x_pos, cell in enumerate(row)
            ) for cell_y_pos, row in enumerate(self._cells)
        ))

    def __hash__(self) -> int:
        total = 0

        for i, row in enumerate(self._cells):
            for j, cell in enumerate(row):
                if cell:
                    total += 1 << (i * self._width + j)

        return total

ALL_PIECE_ROTATIONS = Piece.get_all_piece_rotations()

def possibilities(grid: Grid, cache: dict):
    """
    Gets the number of different possible ways to fill
    the remainder of the Grid
    """

    total = 0

    # TODO: Fix naïvety of scanning x/y
    for y_pos in range(grid.width):
        for x_pos in range(grid.length):
            for piece in ALL_PIECE_ROTATIONS:
                new_grid = grid.place(piece, (x_pos, y_pos))
                if new_grid is None:
                    pass
                elif new_grid in cache:
                    total += cache[new_grid]
                else:
                    total += possibilities(new_grid, cache)

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
    empty_grid = Grid(width, length)

    # The Final result will be stored in the empty Grid state
    return possibilities(empty_grid, grid_states)

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
