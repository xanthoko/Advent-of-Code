from math import prod
from typing import List

from utils import get_input_text


def get_input_list() -> List[List[int]]:
    input_text = get_input_text(9)
    return [[int(x) for x in y] for y in input_text.split('\n')]


def get_sum_of_risk() -> int:
    total_risk = 0
    width, height = len(heightmap[0]), len(heightmap)

    for y in range(height):
        for x in range(width):
            neighbors = [
                heightmap[y - dy][x - dx]
                for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]
                if 0 <= y - dy < height and 0 <= x - dx < width
            ]
            if (el := heightmap[y][x]) < min(neighbors):
                total_risk += el + 1

    return total_risk


def get_basins_length() -> int:
    basin_lenghts = []
    width, height = len(heightmap[0]), len(heightmap)
    seen = set()  # (y, x)

    def _get_basin_length(y: int, x: int):
        if (y, x) in seen or heightmap[y][x] == 9:
            return 0

        # current location
        seen.add((y, x))
        basin_legth = 1

        # right
        if x < len(heightmap[0]) - 1:
            basin_legth += _get_basin_length(y, x + 1)
        # down
        if y < len(heightmap) - 1:
            basin_legth += _get_basin_length(y + 1, x)
        # left
        if x:
            basin_legth += _get_basin_length(y, x - 1)
        # up
        if y:
            basin_legth += _get_basin_length(y - 1, x)

        return basin_legth

    basin_lenghts = [
        _get_basin_length(y, x) for y in range(height) for x in range(width)
    ]

    return prod(sorted(basin_lenghts, reverse=True)[:3])


heightmap = get_input_list()

risk = get_sum_of_risk()
print(f'Risk: {risk}')

basins = get_basins_length()
print(f'Basin length sum: {basins}')
