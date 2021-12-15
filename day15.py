import operator
from dataclasses import dataclass


@dataclass
class Node:
    value: int
    row: int
    col: int


def find_lowest_risk(cavern, rows, cols):
    discovered_nodes = [Node(0, 0, 0)]
    visited_nodes = set()

    while True:
        discovered_nodes.sort(key=operator.attrgetter('value'))
        current = discovered_nodes.pop(0)
        row = current.row
        col = current.col

        if row == rows - 1 and col == cols - 1:
            return current.value

        visited_nodes.add((row, col))
        current_value = current.value
        for new_position in [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]:
            new_row = new_position[0]
            new_col = new_position[1]

            if 0 <= new_row < rows and 0 <= new_col < cols:
                new_value = cavern[new_row][new_col]
                if (new_row, new_col) not in visited_nodes:
                    for node in discovered_nodes:
                        if node.row == new_row and node.col == new_col:
                            node.value = min(node.value, current_value + new_value)
                            break
                    else:
                        discovered_nodes.append(Node(value=current_value + new_value, row=new_row, col=new_col))


with open('input-files/day15.txt') as f:
    cave = [[int(number) for number in row] for row in f.read().splitlines()]

row_num = len(cave)
col_num = len(cave[0])

cave_risk = find_lowest_risk(cave, row_num, col_num)
print("Problem 1: " + str(cave_risk))


big_cave = [[0 for number in range(col_num * 5)] for row in range(row_num * 5)]

big_row_num = len(big_cave)
big_col_num = len(big_cave[0])

for row in range(big_row_num):
    for col in range(big_col_num):
        row_additions = row // row_num
        col_additions = col // col_num

        new_number = cave[row % row_num][col % col_num]
        for i in range(row_additions + col_additions):
            new_number = 1 if new_number == 9 else new_number + 1

        big_cave[row][col] = new_number

big_cave_risk = find_lowest_risk(big_cave, big_row_num, big_col_num)
print("Problem 2: " + str(big_cave_risk))
