def binary_to_num(binary_string):
    number = 0
    string_length = len(binary_string)
    for i, digit in enumerate(binary_string):
        if int(digit) == 1:
            number += 2 ** (string_length - i - 1)
    return number


def find_rating(data, choose_majority):
    digit_count = len(data[0])
    candidate_idx = range(0, len(data))
    for digit_position in range(digit_count):
        ones = []
        zeros = []
        digit_sum = 0
        for line in candidate_idx:
            if int(data[line][digit_position]) == 1:
                ones.append(line)
                digit_sum += 1
            else:
                zeros.append(line)
                digit_sum -= 1
        more_ones = digit_sum >= 0
        if (choose_majority and more_ones) or (not choose_majority and not more_ones):
            candidate_idx = ones
        else:
            candidate_idx = zeros
        if len(candidate_idx) == 1:
            return binary_to_num(data[candidate_idx[0]])


with open('input-files/day3.txt') as f:
    report = f.read().splitlines()

oxygen = find_rating(report, choose_majority=True)
carbondioxide = find_rating(report, choose_majority=False)

print(oxygen * carbondioxide)
