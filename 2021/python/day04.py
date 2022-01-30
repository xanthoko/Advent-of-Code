import numpy
from typing import List, Tuple

from utils import get_input_text


def get_input_list() -> Tuple[List[int], numpy.ndarray]:
    input_text = get_input_text(4)
    splited_str_input_list = input_text.strip().split('\n\n')

    numbers_drawn = splited_str_input_list.pop(0)
    numbers_drawn = list(map(int, numbers_drawn.split(',')))

    # slitted_str_input_list contains the boards
    boards = [x.split('\n') for x in splited_str_input_list]
    boards = _format_boards(boards)
    return numbers_drawn, boards


def _format_boards(boards: List[str]):
    formated_boards = []
    for board in boards:
        b11 = [x.split(' ') for x in board]
        b111 = [[int(x) for x in y if x] for y in b11]
        formated_boards.append(numpy.array(b111))
    return formated_boards


def get_final_score_on_first_winning_board(numbers_drawn: int,
                                           boards: numpy.ndarray) -> int:
    for number in numbers_drawn:
        for i in range(len(boards)):
            boards[i] = _mark_number_in_board(boards[i], number)

            if _check_if_board_wins(boards[i]):
                return _calculate_final_score(boards[i], number)


def get_final_score_on_last_winning_board(numbers_drawn: int,
                                          boards: numpy.ndarray) -> int:
    winners = []
    last_winner = None

    for number in numbers_drawn:
        for i in range(len(boards)):
            # ignore past winners
            if i in winners:
                continue
            boards[i] = _mark_number_in_board(boards[i], number)

            if _check_if_board_wins(boards[i]):
                last_winner = boards[i]
                winners.append(i)
                if len(winners) == len(boards):
                    return _calculate_final_score(last_winner, number)

    return _calculate_final_score(last_winner, number)


def _mark_number_in_board(board: numpy.ndarray, number_drawn: int):
    return numpy.where(board == number_drawn, -1, board)


def _check_if_board_wins(board: numpy.ndarray):
    dim = board.shape[0]
    return -dim in numpy.sum(board, axis=0) or -dim in numpy.sum(board, axis=1)


def _calculate_final_score(board: numpy.ndarray, number_drawn: int) -> int:
    unmarked_sum = numpy.sum(board, where=board != -1)
    final_score = unmarked_sum * number_drawn
    return final_score


def solve():
    numbers_drawn, boards = get_input_list()

    # PART 1
    final_score_1 = get_final_score_on_first_winning_board(numbers_drawn, boards)
    print(f'Final score: {final_score_1}')

    # PART 2
    final_score_2 = get_final_score_on_last_winning_board(numbers_drawn, boards)
    print(f'Final score: {final_score_2}')


if __name__ == '__main__':
    solve()
