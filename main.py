#!/usr/bin/env python3

"""
Etude 9 - Sir Tet's Carpets
Authors: Daniel Thomson, Levi Faid, Nathan Hardy, Rebecca Wilson
"""

import sys

def main():
    for unstripped_line in sys.stdin.readlines():
        line = unstripped_line.strip()

        if line.startswith('#') or line == '':
            continue

        print(line)

        result = 0 # TODO: Actually do something

        print('# {}'.format(result))

if __name__ == '__main__':
    main()
