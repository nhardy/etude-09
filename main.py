#!/usr/bin/env python3

"""
Etude 9 - Sir Tet's Carpets
Authors: Daniel Thomson, Levi Faid, Nathan Hardy, Rebecca Wilson
"""

import sys

def result(width: int, length: int) -> int:
    """
    Returns the number of combinations of carpets possible for
    a carpet of dimensions (width * length)
    """

    if width * length % 4 != 0:
        return 0

    return NotImplemented

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
