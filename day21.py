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
        jumps = (3 * dice_roll + 1 + 2 + 3) % 100
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
    win_score = 21
    state_counts = {(p1_start, 0, p2_start, 0, True): 1}  # (p1_pos, p1_score, p2_pos, p2_score, is_p1_turn)
    single_turn_outcomes = [(3, 1), (4, 3), (5, 6), (6, 7), (7, 6), (8, 3), (9, 1)]  # (dice roll sum, universe splits)

    while state_counts:
        current_state, count = state_counts.popitem()
        p1_pos, p1_score, p2_pos, p2_score, is_p1_turn = current_state
        for roll, splits in single_turn_outcomes:
            if is_p1_turn:
                p1_new_pos, p1_new_score = calculate_next_position_and_score(p1_pos, p1_score, roll)
                if p1_new_score >= win_score:
                    p1_wins += count * splits
                else:
                    new_state = (p1_new_pos, p1_new_score, p2_pos, p2_score, not is_p1_turn)
                    state_counts[new_state] = state_counts.get(new_state, 0) + count * splits
            else:
                p2_new_pos, p2_new_score = calculate_next_position_and_score(p2_pos, p2_score, roll)
                if p2_new_score >= win_score:
                    p2_wins += count * splits
                else:
                    new_state = (p1_pos, p1_score, p2_new_pos, p2_new_score, not is_p1_turn)
                    state_counts[new_state] = state_counts.get(new_state, 0) + count * splits
    return p1_wins, p2_wins


def main():
    p1_start, p2_start = read_file('input-files/day21.txt')
    p1_score, p2_score, dice_roll = play_deterministic(p1_start, p2_start)
    losing_score = min(p1_score, p2_score)
    print(f"Problem 1: {losing_score * dice_roll}")

    p1_wins, p2_wins = play_quantum(p1_start, p2_start)
    print(f"Problem 2: {max(p1_wins, p2_wins)}")


if __name__ == "__main__":
    main()
