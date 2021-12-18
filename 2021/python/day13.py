from typing import List, Tuple, Set

from utils import get_input_text

EXAMPLE_INPUT = '''\
6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5'''
# EXPECTED_1 = 17
# EXPECTED_2 =


def get_input_data(example=False) -> Tuple[Set[Tuple[int, int]], List[str]]:
    if example:
        input_text = EXAMPLE_INPUT
    else:
        input_text = get_input_text(13)

    coords, instructions = map(lambda x: x.split('\n'), input_text.split('\n\n'))
    grid = set(tuple(map(int, x.split(','))) for x in coords)

    return grid, instructions


grid, instructions = get_input_data(False)


def solve_1() -> int:
    first_instruction = instructions[0]  # fold along {axis}={value}
    axis, value = first_instruction.split()[2].split('=')
    value = int(value)
    index = 1 if axis == 'y' else 0

    tgrid = set()
    for coord in grid:
        new_coords = list(coord)
        if coord[index] > value:
            new_coords[index] = value - (coord[index] - value)
        tgrid.add(tuple(new_coords))

    return len(tgrid)


def solve_2() -> None:
    grid_2 = grid.copy()

    for instruction in instructions:
        axis, value = instruction.split()[2].split('=')
        value = int(value)
        index = 1 if axis == 'y' else 0

        tgrid = set()
        for coord in grid_2:
            new_coords = list(coord)
            if coord[index] > value:
                new_coords[index] = value - (coord[index] - value)
            tgrid.add(tuple(new_coords))
        grid_2 = tgrid

    _pprint(grid_2)


def _pprint(grid: Set[Tuple[int, int]]) -> None:
    max_x = max([x[0] for x in grid])
    max_y = max([x[1] for x in grid])

    for y in range(max_y + 1):
        for x in range(max_x + 1):
            if (x, y) in grid:
                print('#', end='')
            else:
                print('.', end='')
        print()


def solve():
    # part 1
    part_1 = solve_1()
    print(f'Part 1: {part_1}')

    # part 2
    solve_2()


if __name__ == '__main__':
    solve()
