from __future__ import annotations

import heapq
from collections import defaultdict
from email.generator import Generator
from typing import Generator
from typing import List
from typing import NamedTuple
from typing import Optional
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
# EXPECTED_1 = 12521
# EXPECTED_2 = 44169


class Amphipod(NamedTuple):
    ind: int
    type: str
    position: int
    room: int
    depth: int

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
        return self.room * 2 + 2 if self._is_in_room() else self.position

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


def get_input_data(example: Optional[bool] = False) -> List[Amphipod]:
    if example:
        input_text = EXAMPLE_INPUT
    else:
        input_text = get_input_text(23)

    lines = input_text.strip().splitlines()

    amphis = []
    for i in range(4):
        amphis.append(Amphipod(i * 2, lines[2][3 + i * 2], None, i, 1))
        amphis.append(Amphipod(i * 2 + 1, lines[3][3 + i * 2], None, i, 2))

    return amphis


_amphis = get_input_data()
restricted_hallway_pos = (2, 4, 6, 8)
# destination_map = {0: 'A', 1: 'B', 2: 'C', 3: 'D'}
destination_map = {'A': 0, 'B': 1, 'C': 2, 'D': 3}


def print_map(amphis: List[Amphipod]) -> None:
    grid = """
#############
#...........#
###.#.#.#.###
  #.#.#.#.#
  ######### """.strip()
    grid = [list(line) for line in grid.split('\n')]

    for amphi in amphis:
        if amphi.room is not None:
            grid[amphi.depth + 1][amphi.room * 2 + 3] = amphi.type
        else:
            grid[1][amphi.position + 1] = amphi.type

    print('\n'.join(''.join(line) for line in grid))
    print()


def _can_amphi_move_outside_of_room(amphi: Amphipod,
                                    amphis: List[Amphipod]) -> bool:
    assert amphi._is_in_room()

    if amphi.depth == 1:
        return True

    # amphipod in same room
    roomate = [x for x in amphis if x.room == amphi.room and x.depth == 1]
    return len(roomate) == 0


def _is_amphi_settled(amphi: Amphipod, amphis: List[Amphipod]) -> bool:
    if amphi.destination_room != amphi.room:  # not in destination room
        return False

    # is in bottom of distination room
    assert amphi.position is None, 'Amphi in room has position not None'
    if amphi.depth == 2:
        return True

    # roomates must be the same type
    roomates = [x for x in amphis if x.room == amphi.room and x.depth == 2]
    assert len(roomates) > 0, 'Top amphi has no roomate'
    return roomates[0].type == amphi.type


def _get_amphis_positions_in_hall(amphis: List[Amphipod]) -> Set[int]:
    return set(x.position for x in amphis if x.position is not None)


def _can_amphi_move_in_room(amphi: Amphipod, amphis: List[Amphipod],
                            room: int) -> Tuple[bool, int]:
    assert room == amphi.destination_room

    amphis_in_this_room = [x for x in amphis if x.room == room]
    if len(amphis_in_this_room) == 0:
        return True, 2
    elif len(amphis_in_this_room) == 2:
        # full
        return False, -1
    else:
        roomate = amphis_in_this_room[0]
        # must be the same type
        return roomate.type == amphi.type, 1


def get_next_state(
    state: Tuple[int, List[Amphipod]]
) -> Generator[Tuple[int, List[Amphipod]], None, None]:
    cost, amphipods = state

    for i, amphi in enumerate(amphipods):
        # continue if amphi cannot move outside of the room
        if amphi._is_in_room() and not _can_amphi_move_outside_of_room(
                amphi, amphipods):
            continue

        # or if amphi is settled in
        if _is_amphi_settled(amphi, amphipods):
            continue

        out_cost = amphi.depth if amphi._is_in_room() else 0
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


def detect_end(amphis: List[Amphipod]) -> bool:
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

end_apods: List[Amphipod] = []
ans = None

pq = [start_state]
ss = 0
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

    ss += 1
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

print(ans)
