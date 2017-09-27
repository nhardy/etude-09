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
            cls('Square', ((True, True,), (True, True,),), 1),
            # 1x4
            cls('Long', ((True, True, True, True,),), 2),
            # s
            cls('S', ((False, True, True,), (True, True, False,),), 4),
            # z
            cls('Z', ((True, True, False,), (False, True, True,),), 4),
            # L
            cls('L', ((True, True, True,), (True, False, False,),), 4),
            # J
            cls('J', ((True, False, False,), (True, True, True,),), 4),
            # T
            cls('T', ((True, True, True,), (False, True, False,),), 4),
        ]

    @classmethod
    def get_all_piece_rotations(cls: 'Piece') -> List[Type['Piece']]:
        """
        Returns a list of all Pieces and their unique rotations
        """

        return [r for p in cls.get_all() for r in p.get_rotations()]

    def __init__(self, name: str, locations: Tuple[Tuple[bool]], rotations: int):
        self._name = name
        self.locations = locations
        self._rotations = rotations

    def first_filled_y(self) -> int:
        for x_pos in range(len(self.locations[0])):
            for y_pos in range(len(self.locations)):
                if self.locations[y_pos][x_pos]:
                    return y_pos

    def get_rotations(self) -> List['Piece']:
        """
        Returns all the rotations for the current Piece
        """

        rotations = [self]
        tmp = self

        for _ in range(self._rotations - 1):
            tmp = Piece(self._name, Piece.rotate(tmp.locations), self._rotations)
            rotations.append(tmp)

        return rotations

    def __str__(self):
        return self._name

class Grid:
    """
    Abstraction useful for dealing with Grid state.
    It is important to note that all properties are immuntable.
    """

    @classmethod
    def filled(cls: 'Grid', width: int, length: int) -> 'Grid':
        """
        Returns a filled Grid of the given size
        """

        return cls(width, length, tuple(tuple(True for _ in range(length)) for _ in range(width)))

    def __init__(self, width: int, length: int, cells: Tuple[Tuple[bool, ...], ...]=None):
        self._width = width
        self._length = length

        # We're specifically using a tuple of tuples here to
        # enforce immutability
        self.cells = cells if cells is not None else tuple(
            tuple(False for _ in range(length)) for _ in range(width)
        )

    @property
    def width(self):
        """
        Gets the width
        """

        return self._width

    @property
    def length(self):
        """
        Gets the length
        """

        return self._length

    def first_empty(self) -> Optional[Tuple[int, int]]:
        """
        Gets the (x, y) coordinate of the first empty cell in the Grid
        """

        for x_pos in range(self._length):
            for y_pos in range(self._width):
                if not self.cells[y_pos][x_pos]:
                    return (x_pos, y_pos)

    def place(self, piece: Piece, coords: Tuple[int, int]) -> Optional['Grid']:
        """
        Tries to place the piece at position (x, y).
        If this fails, returns None.
        """

        x_pos, y_pos = coords
        piece_locations = piece.locations

        if y_pos < 0 or len(piece_locations) + y_pos > self._width:
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
                    if self.cells[cell_y_pos][cell_x_pos]:
                        return None

                    changes.add((cell_x_pos, cell_y_pos))

        return Grid(self._width, self._length, tuple(
            tuple(
                cell or (False if (cell_x_pos, cell_y_pos) not in changes else True) for cell_x_pos, cell in enumerate(row)
            ) for cell_y_pos, row in enumerate(self.cells)
        ))

    def __hash__(self) -> int:
        total = 0

        for i, row in enumerate(self.cells):
            for j, cell in enumerate(row):
                if cell:
                    total += 1 << (i * self._width + j)

        return total

    def __eq__(self, other: Type['Grid']):
        return self.cells == other.cells

    def __str__(self):
        return '\n'.join([
            ''.join(['x' if cell else '?' for cell in row]) for row in self.cells
        ])

ALL_PIECE_ROTATIONS = Piece.get_all_piece_rotations()

def possibilities(grid: Type[Grid], cache: dict):
    """
    Gets the number of different possible ways to fill
    the remainder of the Grid
    """

    total = 0
    first_empty = grid.first_empty()

    if first_empty is not None:
        x_pos, y_pos = first_empty

        for piece in ALL_PIECE_ROTATIONS:
            first_filled_y = piece.first_filled_y()
            new_grid = grid.place(piece, (x_pos, y_pos - first_filled_y))
            if new_grid is not None:
                subtotal = None
                if new_grid in cache:
                    subtotal = cache[new_grid]
                else:
                    subtotal = possibilities(new_grid, cache)
                if subtotal is not None:
                    total += subtotal

    cache[grid] = total
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
    filled_grid = Grid.filled(width, length)
    grid_states[filled_grid] = 1
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
