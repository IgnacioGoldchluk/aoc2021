import numpy as np

MARKED = -1
INVALID = -999
SHAPE = (5, 5)


def parse_input(filename: str):
    with open(filename, "r") as f:
        contents = f.read()

    bingo_sequence, *boards = contents.split("\n\n")
    bingo_sequence = [int(num) for num in bingo_sequence.split(",")]
    boards_list = [np.array(list(map(int, board.split()))).reshape(SHAPE) for board in boards]
    return bingo_sequence, boards_list


def has_winner_row(board):
    return any(all(val == MARKED for val in row) for row in board)


def has_winner_column(board):
    return has_winner_row(board.T)


def is_winner(board) -> bool:
    return has_winner_row(board) or has_winner_column(board)


def cross_number(number, board):
    board[board == number] = MARKED


def board_score_get(number, board):
    board[board == MARKED] = 0
    return np.sum(np.concatenate(board)) * number


def set_board_as_invalid(board):
    board[board < 99] = INVALID
    board[board == MARKED] = INVALID


def get_winners_score(bingo_sequence, boards):
    winners_score = []
    for number in bingo_sequence:
        _ = [cross_number(number, board) for board in boards]
        for board in boards:
            if is_winner(board):
                winners_score.append(board_score_get(number, board))
                set_board_as_invalid(board)
    return winners_score


if __name__ == "__main__":
    bingo_sequence, boards = parse_input("aoc_2021/2021_4.txt")
    first, *_, last = get_winners_score(bingo_sequence, boards)
    print(first, last)
