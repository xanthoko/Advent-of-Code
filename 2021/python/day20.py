from functools import partial
from typing import Tuple, Generator
from collections import defaultdict

from utils import get_input_text

EXAMPLE_INPUT = '''\
..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..##
#..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###
.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#.
.#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#.....
.#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#..
...####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.....
..##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###
'''
# EXPECTED_1 = 35
# EXPECTED_2 = 3351

input_text = get_input_text(20)
# input_text = EXAMPLE_INPUT
algorithm, image = input_text.split('\n\n')
# algorithm = ''.join(algorithm.splitlines()) # NOTE: only for example

grid = defaultdict(int)
for y, lines in enumerate(image.splitlines()):
    for x, c in enumerate(lines):
        if c == '#':
            grid[(y, x)] = 1


def _get_adjacent(
        pos: Tuple[int, int]) -> Generator[Tuple[int, int], None, None]:
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            yield pos[0] + dy, pos[1] + dx


def enhance_image(image: defaultdict, turn: int) -> defaultdict:
    min_y = min(image.keys(), key=lambda x: x[0])[0]
    max_y = max(image.keys(), key=lambda x: x[0])[0]
    min_x = min(image.keys(), key=lambda x: x[1])[1]
    max_x = max(image.keys(), key=lambda x: x[1])[1]

    if algorithm[0] == '#' and algorithm[-1] == '.':
        new_image = defaultdict(partial(lambda q: int(q % 2 == 0), q=turn))
    else:
        new_image = defaultdict(int)

    for y in range(min_y - 2, max_y + 3):
        for x in range(min_x - 2, max_x + 3):
            pos = (y, x)
            binary_number_s = ''
            for ad in _get_adjacent(pos):
                binary_number_s += '1' if image[ad] else '0'

            algo_index = int(binary_number_s, 2)
            new_value = algorithm[algo_index]
            new_image[pos] = int(new_value == '#')

    return new_image


def solve_1() -> int:
    current_image = grid.copy()
    for i in range(2):
        current_image = enhance_image(current_image, i)

    return sum(current_image.values())


def solve_2() -> int:
    current_image = grid.copy()
    for i in range(50):
        current_image = enhance_image(current_image, i)

    return sum(current_image.values())


def solve():
    part_1 = solve_1()
    print(f'Part 1: {part_1}')

    part_2 = solve_2()
    print(f'Part 2: {part_2}')


if __name__ == '__main__':
    solve()
