import math

with open('input-files/day7.txt') as f:
    crab_positions = list(map(int, f.read().split(',')))

crab_positions.sort()

highest_position = crab_positions[-1]
min_fuel = math.inf

for current_position in range(0, highest_position + 1):
    current_fuel = 0
    for crab_position in crab_positions:
        if crab_position > current_position:
            distance = crab_position - current_position
        else:
            distance = current_position - crab_position
        current_fuel += sum(range(distance + 1))

    min_fuel = min(min_fuel, current_fuel)

print(min_fuel)
