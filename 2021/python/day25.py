from typing import Tuple, Optional, Set

from utils import get_input_text

EXAMPLE_INPUT = '''\
v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>
'''
# EXPECTED_1 = 58


def get_input_data(
    example: Optional[bool] = False
) -> Tuple[Set[Tuple[int, int]], Set[Tuple[int, int]], int, int]:
    if example:
        input_text = EXAMPLE_INPUT
    else:
        input_text = get_input_text(25)

    easts = set()
    souths = set()
    for y, lines in enumerate(input_text.strip().splitlines()):
        for x, c in enumerate(lines):
            if c == '>':
                easts.add((y, x))
            elif c == 'v':
                souths.add((y, x))

    return easts, souths, y + 1, x + 1


easts, souths, height, width = get_input_data()


def solve_1() -> int:
    global easts
    global souths
    steps = 0

    while True:
        new_easts = set()
        new_souths = set()
        cucumber_moved = False

        # move easts
        for east in easts:
            adj = (east[0], (east[1] + 1) % width)
            if adj not in easts and adj not in souths:
                cucumber_moved = True
                new_easts.add(adj)
            else:
                new_easts.add(east)

        # move souths
        for south in souths:
            adj = ((south[0] + 1) % height, south[1])
            if adj not in new_easts and adj not in souths:
                new_souths.add(adj)
            else:
                new_souths.add(south)

        # update grid
        easts = new_easts
        souths = new_souths

        steps += 1
        if not cucumber_moved:
            break

    return steps


def solve():
    part_1 = solve_1()
    print(f'Part 1: {part_1}')


if __name__ == '__main__':
    solve()
