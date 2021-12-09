with open('input-files/day9.txt') as f:
    heightmap = [[int(number) for number in row] for row in f.read().splitlines()]

col_num = len(heightmap)
row_num = len(heightmap[0])

risk_level = 0
for i, row in enumerate(heightmap):
    for j, number in enumerate(row):
        is_low_point = True
        for k in range(i-1, i+2):
            for l in range(j-1, j+2):
                if 0 <= k < row_num and 0 <= l < col_num:
                    if heightmap[k][l] < number:
                        is_low_point = False
        if is_low_point:
            risk_level += number + 1

print(risk_level)
