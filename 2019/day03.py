from typing import Tuple, Set, List

from utils import get_input_text, get_example_input_text

input_text = get_input_text(3)
input_text = get_example_input_text()
paths = list(map(lambda x: x.split(','), input_text.split('\n')))


def create_trace(path: List[str]) -> Set[Tuple[int, int]]:
    DIRECTION_MAP = {'R': (1, 0), 'L': (-1, 0), 'U': (0, -1), 'D': (0, 1)}
    trace = set()
    pos = (0, 0)
    for instruction in path:
        direction = instruction[0]
        distance = int(instruction[1:])
        dx, dy = DIRECTION_MAP[direction]
        for _ in range(distance):
            pos = (pos[0] + dx, pos[1] + dy)
            trace.add(pos)
    return trace


def _get_manhatan(pos: Tuple[int, int]) -> int:
    return abs(pos[0]) + abs(pos[1])


trace_1 = create_trace(paths[0])
trace_2 = create_trace(paths[1])
interesection_points = trace_1 & trace_2

man_distances = [_get_manhatan(x) for x in interesection_points]
print(f'[PART 1] The closes distance is {min(man_distances)}')
