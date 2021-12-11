import pytest

from utils import get_input_text, get_example_input_text

EXPECTED_1 = None
EXPECTED_2 = None


def get_input_data(example=False):
    if example:
        input_text = get_example_input_text()
    else:
        input_text = get_input_text(10)
    # TODO: implement code here
    return input_text


lines = get_input_data()


def solve_part_1():
    return


def solve_part_2():
    pass


@pytest.mark.parametrize(
    ('input', 'expected'),
    ((get_input_data(example=True), EXPECTED_1), ),
)
def test_part_1(input: str, expected: int) -> None:
    assert solve_part_1(input) == expected


@pytest.mark.parametrize(
    ('input', 'expected'),
    ((get_input_data(example=True), EXPECTED_2), ),
)
def test_part_2(input: str, expected: int) -> None:
    assert solve_part_2(input) == expected


def main():
    # part 1
    part_1 = solve_part_1(lines)
    print(f'Part 1: {part_1}')

    # part 2
    part2 = solve_part_2(lines)
    print(f'Part 2: {part2}')


if __name__ == '__main__':
    main()
