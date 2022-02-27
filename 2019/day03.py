from __future__ import annotations

import sys

from utils import get_input_text

input_text = get_input_text(3)
paths = list(map(lambda x: x.split(','), input_text.split('\n')))
print()


def create_trace(
        path: list[str]) -> tuple[set[tuple[int, int]], dict[tuple[int, int], int]]:
    DIRECTION_MAP = {'R': (1, 0), 'L': (-1, 0), 'U': (0, -1), 'D': (0, 1)}
    trace = set()
    steps_map: dict[tuple[int, int], int] = {}
    steps = 0
    pos = (0, 0)
    for instruction in path:
        direction = instruction[0]
        distance = int(instruction[1:])
        dx, dy = DIRECTION_MAP[direction]
        for _ in range(distance):
            pos = (pos[0] + dx, pos[1] + dy)
            trace.add(pos)
            steps += 1
            if pos not in steps_map:
                steps_map[pos] = steps
    return trace, steps_map


def _get_manhatan(pos: tuple[int, int]) -> int:
    return abs(pos[0]) + abs(pos[1])


trace_1, steps_map_1 = create_trace(paths[0])
trace_2, steps_map_2 = create_trace(paths[1])
interesection_points = trace_1 & trace_2

man_distances = [_get_manhatan(x) for x in interesection_points]
print(f'[PART 1] The closest distance is {min(man_distances)}')

min_steps = sys.maxsize
for intersection_point in interesection_points:
    wire_1_steps = steps_map_1[intersection_point]
    wire_2_steps = steps_map_2[intersection_point]
    if (sum_steps := wire_1_steps + wire_2_steps) < min_steps:
        min_steps = sum_steps

print(f'[PART 2] The smallest number of steps is: {min_steps}')
