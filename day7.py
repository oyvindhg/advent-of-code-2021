with open('input-files/day7.txt') as f:
    positions = list(map(int, f.read().split(',')))

crab_positions = dict()
for position in positions:
    if position in crab_positions:
        crab_positions[position] += 1
    else:
        crab_positions[position] = 1

highest_position = max(positions)

current_count = crab_positions.get(0, 0)
right_count = len(positions) - current_count
left_count = 0

current_steps = sum(positions)
min_steps = current_steps

for current_position in range(1, highest_position + 1):
    left_count += current_count
    current_count = crab_positions.get(current_position, 0)
    right_count -= current_count
    current_steps = current_steps + left_count - right_count - current_count
    min_steps = min(min_steps, current_steps)

print(min_steps)
