from typing import Generator, Tuple, Dict

from utils import get_input_text

EXAMPLE_INPUT = '''\
5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526
'''
# EXPECTED_1 = 1656
# EXPECTED_2 = 232


def get_input_data(example=False) -> Dict[Tuple[int, int], int]:
    if example:
        input_text = EXAMPLE_INPUT
    else:
        input_text = get_input_text(11)

    grid = {}
    for y, line in enumerate(input_text.strip().split()):
        for x, c in enumerate(line):
            grid[(int(y), int(x))] = int(c)
    return grid


input_data = get_input_data(False)


def _get_adjacent_cells(y: int, x: int) -> Generator[Tuple[int, int], None, None]:
    for adj_y, adj_x in [(y + j, x + i) for i in (-1, 0, 1) for j in (-1, 0, 1)
                         if i != 0 or j != 0]:
        if (adj_y, adj_x) in input_data:
            yield adj_y, adj_x


def solve_1() -> int:
    flashes = 0
    input_1 = input_data.copy()

    for day in range(100):
        flashing_octopuses = []
        for coords in input_1:
            input_1[coords] += 1
            if input_1[coords] > 9:
                flashing_octopuses.append(coords)
                input_1[coords] = 0

        todo = flashing_octopuses.copy()
        while todo:
            coords = todo.pop()
            for adj in _get_adjacent_cells(*coords):
                input_1[adj] += 1
                if input_1[adj] > 9:
                    todo.append(adj)
                    flashing_octopuses.append(adj)
                    input_1[adj] = 0

        flashes += len(flashing_octopuses)
        for fo in flashing_octopuses:
            input_1[fo] = 0

    return flashes


def solve_2() -> int:
    flashes = 0
    input_1 = input_data.copy()

    counter = 0
    while True:
        flashing_octopuses = []
        for coords in input_1:
            input_1[coords] += 1
            if input_1[coords] > 9:
                flashing_octopuses.append(coords)
                input_1[coords] = 0

        todo = flashing_octopuses.copy()
        while todo:
            coords = todo.pop()
            for adj in _get_adjacent_cells(*coords):
                input_1[adj] += 1
                if input_1[adj] > 9:
                    todo.append(adj)
                    flashing_octopuses.append(adj)
                    input_1[adj] = 0

        if len(flashing_octopuses) == len(input_1):
            break
        flashes += len(flashing_octopuses)
        for fo in flashing_octopuses:
            input_1[fo] = 0

        counter += 1
    return counter + 1


def solve():
    # part 1
    part_1 = solve_1()
    print(f'Part 1: {part_1}')

    # part 2
    part_2 = solve_2()
    print(f'Part 1: {part_2}')


if __name__ == '__main__':
    solve()
