with open('input-files/day9.txt') as f:
    heightmap = [[int(number) for number in row] for row in f.read().splitlines()]

row_num = len(heightmap)
col_num = len(heightmap[0])

risk_level = 0
for i, row in enumerate(heightmap):
    for j, number in enumerate(row):
        is_low_point = True
        for new_point in [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]:
            if 0 <= new_point[0] < row_num and 0 <= new_point[1] < col_num:
                if heightmap[new_point[0]][new_point[1]] <= number:
                    is_low_point = False
        if is_low_point:
            risk_level += number + 1

print(risk_level)
