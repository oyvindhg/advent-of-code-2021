from collections import defaultdict
import numpy as np


def parse_input(bingo_input):
    draws = []
    boards = []
    board = []
    row = 0
    for i, line in enumerate(bingo_input):
        if i == 0:
            draws = [int(number) for number in line.split(',')]
        elif line:
            row += 1
            row_numbers = [int(number) for number in line.split()]
            board.append(row_numbers)
            if row == 5:
                boards.append(board)
                board = []
                row = 0
    return draws, boards


def create_board_number_dict(boards):
    number_dict = defaultdict(list)
    for board_num, board in enumerate(boards):
        for row_num, row in enumerate(board):
            for col_num, number in enumerate(row):
                number_dict[number].append((board_num, row_num, col_num))
    return number_dict


def calculate_score(win_board, win_board_hits, drawn_number):
    board_score = 0
    for r_num, r in enumerate(win_board_hits):
        for c_num, hit in enumerate(r):
            if hit == 0:
                board_score += win_board[r_num][c_num]
    return board_score * drawn_number


def play_win(draws, boards, board_hits, number_dict):
    for draw in draws:
        hits = number_dict[draw]
        for hit in hits:
            board = hit[0]
            row = hit[1]
            col = hit[2]
            board_hits[board][row][col] = 1
            row_hits = sum(board_hits[board][:, col])
            col_hits = sum(board_hits[board][row][:])
            if row_hits == 5 or col_hits == 5:
                return calculate_score(boards[board], board_hits[board], draw)


def play_lose(draws, boards, board_hits, number_dict):
    board_wins = [0] * len(boards)

    for draw in draws:
        hits = number_dict[draw]
        for hit in hits:
            board = hit[0]
            if board_wins[board] == 0:
                row = hit[1]
                col = hit[2]
                board_hits[board][row][col] = 1
                row_hits = sum(board_hits[board][:, col])
                col_hits = sum(board_hits[board][row][:])
                if row_hits == 5 or col_hits == 5:
                    board_wins[board] = 1
                    if sum(board_wins) == len(boards):
                        return calculate_score(boards[board], board_hits[board], draw)


with open('input-files/day4.txt') as f:
    file_input = f.read().splitlines()

bingo_draws, bingo_boards = parse_input(file_input)

bingo_number_dict = create_board_number_dict(bingo_boards)
bingo_board_hits = np.array([[[0 for col in range(5)] for row in range(5)] for board in range(len(bingo_boards))])

win_score = play_win(bingo_draws, bingo_boards, bingo_board_hits, bingo_number_dict)
print("Problem 1:" + str(win_score))

lose_score = play_lose(bingo_draws, bingo_boards, bingo_board_hits, bingo_number_dict)
print("Problem 2:" + str(lose_score))
