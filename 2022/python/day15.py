from __future__ import annotations

import argparse

from utils import get_input_text

EXAMPLE_INPUT = '''\
Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
'''
EXPECTED_1 = 26
EXPECTED_2 = 56000011

parser = argparse.ArgumentParser(prog='AoC')
parser.add_argument('-p',
                    '--production',
                    required=False,
                    const=True,
                    nargs='?',
                    default=False)
is_production = parser.parse_args().production


def get_input_data() -> None:
    if is_production:
        input_text = get_input_text(15)
    else:
        input_text = EXAMPLE_INPUT
    input_text.strip('\n')
    readings = []
    for reading in input_text.splitlines():
        splt = reading.split(' ')
        s_x = int(splt[2][2:-1])
        s_y = int(splt[3][2:-1])
        b_x = int(splt[8][2:-1])
        b_y = int(splt[9][2:])
        readings.append(((s_x, s_y), (b_x, b_y)))
    return readings


input_data = get_input_data()


def get_manhattan_distance(a: tuple(int, int), b: tuple(int, int)) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def solve_1() -> int:
    target_y = 2000000 if is_production else 10
    safe: set(int) = set()
    for sensor, beacon in input_data:
        distance = get_manhattan_distance(sensor, beacon)
        # safe_x = sorted([sensor[0] - distance, distance + sensor[0]])
        safe_y = sorted([sensor[1] - distance, distance + sensor[1]])

        if safe_y[0] <= target_y <= safe_y[1]:
            t = distance - abs(sensor[1] - target_y)
            nsx = sorted([sensor[0] - t, t + sensor[0]])
            for i in range(nsx[0], nsx[1]):
                safe.add(i)
    return len(safe)


def solve_2() -> int:
    limit = 4000000 if is_production else 20

    safe_zones: list[list(int)] = [[] for _ in range(limit + 1)]
    pairs = sorted(input_data, key=lambda x: x[0][1])

    for sensor, beacon in pairs:
        distance = get_manhattan_distance(sensor, beacon)
        safe_y = sorted([sensor[1] - distance, distance + sensor[1]])

        for y in range(max(0, safe_y[0]), min(limit, safe_y[1]) + 1):
            t = distance - abs(sensor[1] - y)
            safe_x = sorted([sensor[0] - t, t + sensor[0]])
            safe_zones[y].append([max(0, safe_x[0]), min(limit, safe_x[1])])

    for i, row in enumerate(safe_zones):
        row.sort(key=lambda x: x[0])
        t = [row[0]]
        for p in row[1:]:
            if p[0] <= t[-1][1] + 1:
                t[-1][1] = max(t[-1][1], p[1])

        if t[-1][1] != limit:
            return (t[-1][1] + 1) * 4000000 + i


def _validate(expected, actual):
    if not is_production:
        error_msg = f'\033[41mExpected: {expected}. Got: {actual}\033[m'
        assert actual == expected, error_msg


def solve():
    part_1 = solve_1()
    print(f'Part 1: {part_1}')
    _validate(EXPECTED_1, part_1)

    part_2 = solve_2()
    print(f'Part 2: {part_2}')
    _validate(EXPECTED_2, part_2)


if __name__ == '__main__':
    solve()
