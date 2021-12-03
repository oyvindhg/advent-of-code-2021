with open('input-files/day3.txt') as f:
    report = f.read().splitlines()

digit_count = len(report[0])
gamma = 0
epsilon = 0

for digit_position in range(digit_count):
    digit_sum = 0
    for line in range(len(report)):
        if int(report[line][digit_position]) == 1:
            digit_sum += 1
        else:
            digit_sum -= 1
    more_ones = digit_sum > 0
    position_power = digit_count - digit_position - 1
    gamma += 2 ** position_power * more_ones
    epsilon += 2 ** position_power * (not more_ones)

print(gamma * epsilon)
