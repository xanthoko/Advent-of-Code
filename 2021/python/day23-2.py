from __future__ import annotations

import heapq
from collections import defaultdict
from typing import Generator
from typing import List
from typing import NamedTuple
from typing import Set
from typing import Tuple

from utils import get_input_text

EXAMPLE_INPUT = '''\
#############
#...........#
###B#C#B#D###
  #D#C#B#A#
  #D#B#A#C#
  #A#D#C#A#
  #########
'''
# EXPECTED_2 = 44169


class Amphipod(NamedTuple):
    ind: int
    type: str
    position: int | None
    room: int | None
    depth: int | None

    def move_to_room(self, room: int, depth: int) -> Amphipod:
        return self._replace(room=room, depth=depth, position=None)

    def move_to_hallway(self, position) -> Amphipod:
        assert self.position is None  # cannot move hallway -> hallway
        return self._replace(room=None, depth=None, position=position)

    @property
    def destination_room(self) -> int:
        return destination_map[self.type]

    @property
    def location(self) -> int:
        if self.room is None:
            assert self.position is not None
            return self.position
        return self.room * 2 + 2

    @property
    def step(self) -> int:
        return 10**(destination_map[self.type])

    def _is_in_room(self) -> bool:
        return self.room is not None and self.position is None

    def _status(self) -> str:
        return f'Position: {self.position}, Room: {self.room}-{self.depth}'

    def __lt__(self, other):
        return id(self) < id(other)

    def __repr__(self) -> str:
        return f'Amphi: {self.type}'


def get_input_data(example: bool = False) -> List[Amphipod]:
    if example:
        input_text = EXAMPLE_INPUT
    else:
        input_text = get_input_text(23)

    lines = input_text.strip().splitlines()

    amphis = []
    for i in range(4):
        amphis.append(Amphipod(i * 4, lines[2][3 + i * 2], None, i, 1))
        amphis.append(Amphipod(i * 4 + 1, lines[3][3 + i * 2], None, i, 2))
        amphis.append(Amphipod(i * 4 + 2, lines[4][3 + i * 2], None, i, 3))
        amphis.append(Amphipod(i * 4 + 3, lines[5][3 + i * 2], None, i, 4))

    return amphis


_amphis = get_input_data()
restricted_hallway_pos = (2, 4, 6, 8)
destination_map = {'A': 0, 'B': 1, 'C': 2, 'D': 3}


def print_map(amphis: Tuple[Amphipod, ...]) -> None:
    grid_s = """
#############
#...........#
###.#.#.#.###
  #.#.#.#.#
  #.#.#.#.#
  #.#.#.#.#
  ######### """.strip()
    grid = [list(line) for line in grid_s.split('\n')]

    for amphi in amphis:
        if amphi.room is not None and amphi.depth is not None:
            grid[amphi.depth + 1][amphi.room * 2 + 3] = amphi.type
        else:
            assert amphi.position is not None
            grid[1][amphi.position + 1] = amphi.type

    print('\n'.join(''.join(line) for line in grid))
    print()


def _can_amphi_move_outside_of_room(amphi: Amphipod, amphis: Tuple[Amphipod,
                                                                   ...]) -> bool:
    assert amphi._is_in_room()

    if amphi.depth == 1:
        return True

    # amphipods in same room
    roomates = [x for x in amphis if x.room == amphi.room and x != amphi]
    return not any([x.depth < amphi.depth for x in roomates])


def _is_amphi_settled(amphi: Amphipod, amphis: Tuple[Amphipod, ...]) -> bool:
    if amphi.destination_room != amphi.room:  # not in destination room
        return False

    # is in bottom of distination room
    assert amphi.position is None, 'Amphi in room has position not None'
    if amphi.depth == 4:
        return True

    # roomates must be the same type
    roomates = [x for x in amphis if x.room == amphi.room and x != amphi]
    assert len(roomates) > 0, 'Not bottom amphi has no roomate'
    return all([x.type == amphi.type for x in roomates])


def _get_amphis_positions_in_hall(amphis: Tuple[Amphipod, ...]) -> Set[int]:
    return set(x.position for x in amphis if x.position is not None)


def _can_amphi_move_in_room(amphi: Amphipod, amphis: Tuple[Amphipod, ...],
                            room: int) -> Tuple[bool, int]:
    assert room == amphi.destination_room

    amphis_in_this_room = [x for x in amphis if x.room == room]
    if len(amphis_in_this_room) == 0:
        return True, 4
    elif len(amphis_in_this_room) == 4:
        # full
        return False, -1
    else:
        # all must be the same type
        return len(set(
            x.type for x in amphis_in_this_room)) == 1, 4 - len(amphis_in_this_room)


def get_next_state(
    state: Tuple[int, Tuple[Amphipod, ...]]
) -> Generator[Tuple[int, Tuple[Amphipod, ...]], None, None]:
    cost, amphipods = state

    for i, amphi in enumerate(amphipods):
        # continue if amphi cannot move outside of the room
        if amphi._is_in_room() and not _can_amphi_move_outside_of_room(
                amphi, amphipods):
            continue

        # or if amphi is settled in
        if _is_amphi_settled(amphi, amphipods):
            continue

        if amphi._is_in_room():
            assert amphi.depth is not None
            out_cost = amphi.depth
        else:
            out_cost = 0
        location = amphi.location

        other_hallway_amphis = _get_amphis_positions_in_hall(amphipods)

        # look left
        left_index = location - 1
        while left_index > -1:
            if left_index in other_hallway_amphis:  # other amphi blocking
                break

            if left_index in restricted_hallway_pos:
                # check if room is destination
                room_location = left_index // 2 - 1
                if room_location == amphi.destination_room:
                    if (move_t := _can_amphi_move_in_room(amphi, amphipods,
                                                          room_location))[0]:

                        # move to room
                        cost_to_move = (out_cost + abs(location - left_index) +
                                        move_t[1]) * amphi.step
                        new_amphi = amphi.move_to_room(room_location, move_t[1])
                        amphis_copy = list(amphipods)
                        amphis_copy[i] = new_amphi
                        yield cost + cost_to_move, tuple(amphis_copy)
                        break
            else:
                # only go to hallway if not in hallway
                if amphi._is_in_room():

                    # move to hallway
                    cost_to_move = (out_cost +
                                    abs(location - left_index)) * amphi.step
                    new_amphi = amphi.move_to_hallway(left_index)
                    amphis_copy = list(amphipods)
                    amphis_copy[i] = new_amphi
                    yield cost + cost_to_move, tuple(amphis_copy)
            left_index -= 1

        # look right
        right_index = location + 1
        while right_index < 11:
            if right_index in other_hallway_amphis:  # other amphi blocking
                break

            if right_index in restricted_hallway_pos:
                # check if room is destination
                room_location = right_index // 2 - 1
                if room_location == amphi.destination_room:
                    if (move_t := _can_amphi_move_in_room(amphi, amphipods,
                                                          room_location))[0]:

                        # move to room
                        cost_to_move = (out_cost + abs(location - right_index) +
                                        move_t[1]) * amphi.step
                        new_amphi = amphi.move_to_room(room_location, move_t[1])
                        amphis_copy = list(amphipods)
                        amphis_copy[i] = new_amphi
                        yield cost + cost_to_move, tuple(amphis_copy)
                        break
            else:
                # only go to hallway if not in hallway
                if amphi._is_in_room():

                    # move to hallway
                    cost_to_move = (out_cost +
                                    abs(location - right_index)) * amphi.step
                    new_amphi = amphi.move_to_hallway(right_index)
                    amphis_copy = list(amphipods)
                    amphis_copy[i] = new_amphi
                    yield cost + cost_to_move, tuple(amphis_copy)
            right_index += 1


def detect_end(amphis: Tuple[Amphipod, ...]) -> bool:
    for amphi in amphis:
        if not amphi._is_in_room():
            return False
        if amphi.room != amphi.destination_room:
            return False
    return True


start_state = 0, tuple(_amphis)
breadcrumbs = defaultdict(tuple)

visited = set()
cost = defaultdict(int)

end_apods: Tuple[Amphipod, ...] = tuple()
ans = None

pq = [start_state]
while len(pq) > 0:
    cur_cost, cur_apods = heapq.heappop(pq)

    if cur_apods in visited:
        continue
    visited.add(cur_apods)

    cost[cur_apods] = cur_cost
    if detect_end(cur_apods):
        ans = cur_cost
        end_apods = cur_apods
        break

    for next_state in get_next_state((cur_cost, cur_apods)):
        if next_state[1] in visited:
            continue

        breadcrumbs[next_state[1]] = cur_apods
        heapq.heappush(pq, next_state)

print_map(end_apods)

# cur_apods = end_apods
# while breadcrumbs[cur_apods] != tuple():
#     print(cost[cur_apods])
#     print_map(cur_apods)
#     cur_apods = breadcrumbs[cur_apods]

print(f'Part 2: {ans}')
