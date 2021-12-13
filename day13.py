from dataclasses import dataclass


@dataclass
class FoldInstruction:
    axis: str
    value: int


def print_code(final_points):
    max_x = max(p[0] for p in final_points)
    max_y = max(p[1] for p in final_points)
    for col in range(max_y + 1):
        for row in range(max_x + 1):
            if (row, col) in final_points:
                print('$', end='')
            else:
                print('_', end='')
        print('')


def parse_input(file_input):
    initial_points = []
    fold_instructions = []
    start_fold_instructions = False
    for line in file_input:
        if not line:
            start_fold_instructions = True
        elif not start_fold_instructions:
            numbers = [int(number) for number in line.split(',')]
            initial_points.append((numbers[0], numbers[1]))
        else:
            instruction = line.split()[2].split('=')
            fold_instructions.append(FoldInstruction(str(instruction[0]), int(instruction[1])))
    return initial_points, fold_instructions


with open('input-files/day13.txt') as f:
    raw_input = f.read().splitlines()


points, folds = parse_input(raw_input)

point_set = set(points)
for i, fold in enumerate(folds):
    value = fold.value
    new_point_set = set()
    for point in point_set:
        if fold.axis == 'x':
            distance = point[0] - value
            if distance <= 0:
                new_point_set.add(point)
            else:
                new_point = (value - distance, point[1])
                new_point_set.add(new_point)
        else:
            distance = point[1] - value
            if distance <= 0:
                new_point_set.add(point)
            else:
                new_point = (point[0], value - distance)
                new_point_set.add(new_point)
    point_set = new_point_set
    if i == 0:
        print("Problem 1: " + str(len(point_set)))

print("Problem 2:")
print_code(point_set)
