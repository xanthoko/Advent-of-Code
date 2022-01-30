from collections import defaultdict
from typing import List, Dict, Tuple

from utils import get_input_text


def get_input_list() -> List[str]:
    input_text = get_input_text(5)
    splited_str_input_list = input_text.strip().split('\n')
    return splited_str_input_list


def get_dangerous_areas_1(entries: List[str]) -> int:
    points = defaultdict(int)
    for entry in entries:
        x1, y1, x2, y2 = _get_coordinates(entry)

        if x1 == x2:  # vertical
            for i in range(min(y1, y2), max(y1, y2) + 1):
                points[(x1, i)] += 1
        elif y1 == y2:  # horizontal
            for i in range(min(x1, x2), max(x1, x2) + 1):
                points[(i, y1)] += 1

    return _find_dangerous_areas(points)


def get_dangerous_areas_2(entries: List[str]) -> int:
    points = defaultdict(int)

    for entry in entries:
        x1, y1, x2, y2 = _get_coordinates(entry)

        if x1 == x2:  # vertical
            for i in range(min(y1, y2), max(y1, y2) + 1):
                points[(x1, i)] += 1
        elif y1 == y2:  # horizontal
            for i in range(min(x1, x2), max(x1, x2) + 1):
                points[(i, y1)] += 1
        else:  # diagonal
            if x1 > x2:
                r1 = range(x1, x2 - 1, -1)
            else:
                r1 = range(x1, x2 + 1)
            if y1 > y2:
                r2 = range(y1, y2 - 1, -1)
            else:
                r2 = range(y1, y2 + 1)
            for i, j in zip(r1, r2):
                points[(i, j)] += 1

    return _find_dangerous_areas(points)


def _get_coordinates(entry: str) -> Tuple[int, int, int, int]:
    part1, part2 = entry.split(' -> ')
    x1, y1 = map(int, part1.split(','))
    x2, y2 = map(int, part2.split(','))
    return x1, y1, x2, y2


def _find_dangerous_areas(points: Dict[Tuple[int, int], int]) -> int:
    return len(list(filter(lambda x: x > 1, points.values())))


def solve():
    entries = get_input_list()

    # PART 1
    dangerous_areas_1 = get_dangerous_areas_1(entries)
    print(f'{dangerous_areas_1} dangerous areas')

    # PART 2
    dangerous_areas_2 = get_dangerous_areas_2(entries)
    print(f'{dangerous_areas_2} dangerous areas')


if __name__ == '__main__':
    solve()
