from math import prod
from typing import Generator, Dict, Tuple

from utils import get_input_text


def get_input_grid() -> Dict[Tuple[int, int], int]:
    input_text = get_input_text(9)
    grid = {}
    for y, line in enumerate(input_text.strip().split('\n')):
        for x, c in enumerate(line):
            grid[(y, x)] = int(c)
    return grid


def get_adjacent(y: int, x: int) -> Generator[Tuple[int, int], None, None]:
    yield y - 1, x
    yield y + 1, x
    yield y, x - 1
    yield y, x + 1


def get_sum_of_risk() -> int:
    total_risk = 0
    for (y, x), c in heightmap.items():
        if all(heightmap.get(pt, 9) > c for pt in get_adjacent(y, x)):
            total_risk += c + 1

    return total_risk


def get_basins_length() -> int:
    basin_lenghts = []
    seen = set()  # (y, x)

    def _get_basin_length(y: int, x: int):
        if (y, x) in seen or heightmap.get((y, x), 9) == 9:
            return 0

        # current location
        seen.add((y, x))
        basin_legth = 1

        # right, down, left, up
        basin_legth += _get_basin_length(y, x + 1)
        basin_legth += _get_basin_length(y + 1, x)
        basin_legth += _get_basin_length(y, x - 1)
        basin_legth += _get_basin_length(y - 1, x)

        return basin_legth

    basin_lenghts = [_get_basin_length(pt[0], pt[1]) for pt in heightmap.keys()]
    return prod(sorted(basin_lenghts, reverse=True)[:3])


heightmap = get_input_grid()

risk = get_sum_of_risk()
print(f'Risk: {risk}')

basins = get_basins_length()
print(f'Basin length sum: {basins}')
