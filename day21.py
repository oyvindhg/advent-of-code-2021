from dataclasses import dataclass


def read_file(filepath):
    with open(filepath) as f:
        rows = f.read().splitlines()
    p1_start = int(rows[0].split(':')[1])
    p2_start = int(rows[1].split(':')[1])
    return p1_start, p2_start


def calculate_next_position_and_score(current_position, current_score, jumps):
    position = (current_position + jumps) % 10
    score = current_score + (10 if position == 0 else position)
    return position, score


def play_deterministic(p1_start, p2_start):
    dice_roll = 0
    p1_score = 0
    p2_score = 0
    p1_position = p1_start
    p2_position = p2_start
    is_p1_turn = True

    while p1_score < 1000 and p2_score < 1000:
        jumps = 3 * dice_roll + 1 + 2 + 3
        dice_roll = dice_roll + 3
        if is_p1_turn:
            p1_position, p1_score = calculate_next_position_and_score(p1_position, p1_score, jumps)
        else:
            p2_position, p2_score = calculate_next_position_and_score(p2_position, p2_score, jumps)
        is_p1_turn = not is_p1_turn

    return p1_score, p2_score, dice_roll


def play_quantum(p1_start, p2_start):
    p1_wins = 0
    p2_wins = 0
    count = {(p1_start, p2_start, 0, 0): 1}

    current_state = count.popitem()
    p1_pos, p2_pos, p1_score, p2_score = current_state.key
    # first = calculate_next_position_and_score(c)


def main():
    p1_start, p2_start = read_file('input-files/day21_test.txt')
    p1_score, p2_score, dice_roll = play_deterministic(p1_start, p2_start)
    losing_score = min(p1_score, p2_score)
    print(f"Problem 1: {losing_score * dice_roll}")

    play_quantum(p1_start, p2_start)


if __name__ == "__main__":
    main()
