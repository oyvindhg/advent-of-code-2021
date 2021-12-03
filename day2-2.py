with open('input-files/day2.txt') as f:
    instructions = [instruction_raw.split() for instruction_raw in f.read().splitlines()]

horizontal = 0
depth = 0
aim = 0
for instruction in instructions:
    direction = instruction[0]
    length = int(instruction[1])
    if direction == "forward":
        horizontal += length
        depth += aim * length
    elif direction == "down":
        aim += length
    else:
        aim -= length

print(horizontal * depth)
