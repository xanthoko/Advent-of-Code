from __future__ import annotations
from typing import Tuple
from itertools import cycle
from functools import lru_cache
import collections

from utils import get_input_text

EXAMPLE_INPUT = '''\
Player 1 starting position: 4
Player 2 starting position: 8
'''
# EXPECTED_1 = 739785
# EXPECTED_2 = 444356092776315


def get_input_data(example=False) -> None:
    if example:
        input_text = EXAMPLE_INPUT
    else:
        input_text = get_input_text(21)

    p1_s, p2_s = input_text.strip().splitlines()
    p1 = int(p1_s.split()[-1])
    p2 = int(p2_s.split()[-1])
    return p1, p2


p1, p2 = get_input_data()


class Player:
    def __init__(self, position: int, score=0) -> None:
        self.position = position
        self.score = score

    def move_to_position(self, position: int):
        self.position = position
        self.score += position

    def play(self, dice: DeterDice):
        roll = dice.roll()
        next_position = _get_next_position(self.position, roll)
        self.move_to_position(next_position)


class DeterDice:
    def __init__(self) -> None:
        self.die = cycle(range(1, 101))
        self.total_rolls = 0

    def roll(self) -> int:
        self.total_rolls += 3
        return next(self.die) + next(self.die) + next(self.die)


def _get_next_position(current_position: int, steps: int):
    actual_steps = steps % 10
    next_space = (current_position + actual_steps) % 10
    if next_space == 0:
        next_space = 10
    return next_space


def solve_1() -> int:
    player_1 = Player(p1)
    player_2 = Player(p2)
    dice = DeterDice()

    while player_1.score < 1000 and player_2.score < 1000:
        player_1.play(dice)
        if player_1.score >= 1000:
            break
        player_2.play(dice)

    return min(player_1.score, player_2.score) * dice.total_rolls


die_rolls = collections.Counter(i + j + k for i in (1, 2, 3) for j in (1, 2, 3)
                                for k in (1, 2, 3))


def solve_2() -> int:
    """
    Big thanks to https://github.com/anthonywritescode/aoc2021/blob/main/day21/part2.py
    for the optimizations
    """
    @lru_cache(maxsize=None)
    def compute_win_count(
        p1_pos: int,
        p1_score: int,
        p2_pos: int,
        p2_score: int,
    ) -> Tuple[int, int]:
        p1_wins = p2_wins = 0
        for k, ct in die_rolls.items():
            new_p1_pos = _get_next_position(p1_pos, k)
            new_p1_score = p1_score + new_p1_pos
            if new_p1_score >= 21:
                p1_wins += ct
            else:
                tmp_p2_wins, tmp_p1_wins = compute_win_count(
                    p2_pos,
                    p2_score,
                    new_p1_pos,
                    new_p1_score,
                )
                p1_wins += tmp_p1_wins * ct
                p2_wins += tmp_p2_wins * ct

        return p1_wins, p2_wins

    p1_win, p2_win = compute_win_count(p1, 0, p2, 0)
    return max(p1_win, p2_win)


def solve():
    part_1 = solve_1()
    print(f'Part 1: {part_1}')

    part_2 = solve_2()
    print(f'Part 2: {part_2}')


if __name__ == '__main__':
    solve()
