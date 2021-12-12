import numpy as np

with open('input-files/day9.txt') as f:
    heightmap = [[int(number) for number in row] for row in f.read().splitlines()]

row_num = len(heightmap)
col_num = len(heightmap[0])

low_points = []

risk_level = 0
for i, row in enumerate(heightmap):
    for j, number in enumerate(row):
        is_low_point = True
        for new_point in [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]:
            if 0 <= new_point[0] < row_num and 0 <= new_point[1] < col_num:
                if heightmap[new_point[0]][new_point[1]] <= number:
                    is_low_point = False
        if is_low_point:
            low_points.append((i, j))

basin_sizes = []

for low_point in low_points:
    basin_size = 1
    visited_points = set()
    visited_points.add(low_point)
    stack = [low_point]

    while len(stack) > 0:
        current = stack.pop()
        i = current[0]
        j = current[1]
        for new_point in [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]:
            if 0 <= new_point[0] < row_num and 0 <= new_point[1] < col_num:
                if heightmap[new_point[0]][new_point[1]] < 9 and new_point not in visited_points:
                    basin_size += 1
                    stack.append(new_point)
                    visited_points.add(new_point)
    basin_sizes.append(basin_size)

biggest_basins = sorted(basin_sizes, reverse=True)[:3]

print(np.prod(biggest_basins))
