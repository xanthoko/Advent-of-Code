import sys
from typing import Generator, Dict, Tuple

from utils import get_input_text

EXAMPLE_INPUT = '''\
1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581
'''
# EXPECTED_1 = 40
# EXPECTED_2 = 315


def get_input_data(
        example=False) -> Tuple[Dict[Tuple[int, int], int], int, int]:
    if example:
        input_text = EXAMPLE_INPUT
    else:
        input_text = get_input_text(15)

    grid = {}
    for y, line in enumerate(input_text.strip().splitlines()):
        for x, c in enumerate(line):
            grid[(y, x)] = int(c)
    return grid, y + 1, x + 1


grid, height, width = get_input_data()


def _get_adjacent(position: Tuple[int, int],
                  tmap) -> Generator[Tuple[int, int], None, None]:
    for dy, dx in (-1, 0), (1, 0), (0, -1), (0, 1):
        if (new_pos := (position[0] + dy, position[1] + dx)) in tmap:
            yield new_pos


def solve_1(tile_map, t_height, t_width):
    """Basically dijkstra's algorithm for shortest path"""
    start_node = (0, 0)
    unvisited_nodes = set(tile_map.keys())

    max_value = sys.maxsize
    shortest_path = {x: max_value for x in unvisited_nodes}
    shortest_path[start_node] = 0

    while unvisited_nodes:
        print(len(unvisited_nodes))
        current_min_node = None
        for node in unvisited_nodes:
            if current_min_node is None or shortest_path[node] < shortest_path[
                    current_min_node]:
                current_min_node = node

        for ad in _get_adjacent(current_min_node, tile_map):
            tentative_value = shortest_path[current_min_node] + tile_map[ad]
            if tentative_value < shortest_path[ad]:
                shortest_path[ad] = tentative_value

        unvisited_nodes.discard(current_min_node)

    return shortest_path[(t_height - 1, t_width - 1)]


def _build_full_grid():
    def t(cy, cx):
        ng = {}
        for pos, value in grid.items():
            nv = (value + cy + cx) % 9
            if not nv:
                nv = 9
            new_pos = (pos[0] + (cy * height), pos[1] + (cx * width))
            ng[new_pos] = nv

        return ng

    full_grid = {}
    for y in range(5):
        for x in range(5):
            full_grid.update(t(y, x))

    return full_grid


def solve_2() -> int:
    full_grid = _build_full_grid()
    return solve_1(full_grid, height * 5, width * 5)


def solve():
    part_1 = solve_1(grid, height, width)
    print(f'Part 1: {part_1}')

    part_2 = solve_2()
    print(f'Part 2: {part_2}')


if __name__ == '__main__':
    solve()
