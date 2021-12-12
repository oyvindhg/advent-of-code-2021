with open('input-files/day11.txt') as f:
    energy_levels = [[int(number) for number in row] for row in f.read().splitlines()]

row_num = len(energy_levels)
col_num = len(energy_levels[0])

steps = 0
total_sum = sum([sum(row) for row in energy_levels])

while total_sum > 0:
    steps += 1
    flashed = set()
    stack = []
    for row in range(row_num):
        for col in range(col_num):
            energy_levels[row][col] += 1
            if energy_levels[row][col] > 9:
                stack.append((row, col))
                flashed.add((row, col))

    while len(stack) > 0:
        (row, col) = stack.pop()
        for adj_row in range(row - 1, row + 2):
            for adj_col in range(col - 1, col + 2):
                if 0 <= adj_row < row_num and 0 <= adj_col < col_num and not (adj_row == row and adj_col == col):
                    energy_levels[adj_row][adj_col] += 1
                    if energy_levels[adj_row][adj_col] > 9 and (adj_row, adj_col) not in flashed:
                        stack.append((adj_row, adj_col))
                        flashed.add((adj_row, adj_col))

    for row in range(row_num):
        for col in range(col_num):
            if energy_levels[row][col] > 9:
                energy_levels[row][col] = 0

    total_sum = sum([sum(row) for row in energy_levels])

print(steps)
