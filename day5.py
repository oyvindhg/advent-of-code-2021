from dataclasses import dataclass


@dataclass
class Line:
    x1: int
    y1: int
    x2: int
    y2: int


def parse_input(file_input):
    lines = []
    for line in file_input:
        start, end = line.split(" -> ")
        x1, y1 = start.split(',')
        x2, y2 = end.split(',')
        lines.append(Line(int(x1), int(y1), int(x2), int(y2)))
    return lines


def find_horizontal_and_vertical_overlaps(lines):
    hits = dict()
    overlaps = 0
    for line in lines:
        x1 = line.x1
        x2 = line.x2
        y1 = line.y1
        y2 = line.y2
        if x1 == x2:
            min_y = min(y1, y2)
            max_y = max(y1, y2)
            y_values = list(range(min_y, max_y + 1))
            for y in y_values:
                if (x1, y) in hits:
                    hits[(x1, y)] += 1
                    if hits[(x1, y)] == 2:
                        overlaps += 1
                else:
                    hits[(x1, y)] = 1
        elif y1 == y2:
            min_x = min(x1, x2)
            max_x = max(x1, x2)
            x_values = list(range(min_x, max_x + 1))
            for x in x_values:
                if (x, y1) in hits:
                    hits[(x, y1)] += 1
                    if hits[(x, y1)] == 2:
                        overlaps += 1
                else:
                    hits[(x, y1)] = 1
    return overlaps


def find_overlaps(lines):
    hits = dict()
    overlaps = 0
    for line in lines:
        x1 = line.x1
        x2 = line.x2
        y1 = line.y1
        y2 = line.y2
        if x1 == x2:
            min_y = min(y1, y2)
            max_y = max(y1, y2)
            y_values = list(range(min_y, max_y + 1))
            for y in y_values:
                if (x1, y) in hits:
                    hits[(x1, y)] += 1
                    if hits[(x1, y)] == 2:
                        overlaps += 1
                else:
                    hits[(x1, y)] = 1
        elif y1 == y2:
            min_x = min(x1, x2)
            max_x = max(x1, x2)
            x_values = list(range(min_x, max_x + 1))
            for x in x_values:
                if (x, y1) in hits:
                    hits[(x, y1)] += 1
                    if hits[(x, y1)] == 2:
                        overlaps += 1
                else:
                    hits[(x, y1)] = 1
        else:
            x_iter = 1 if x2 > x1 else -1
            y_iter = 1 if y2 > y1 else -1
            length = y2 - y1 + 1 if y2 > y1 else y1 - y2 + 1
            for i in range(length):
                x = x1 + x_iter * i
                y = y1 + y_iter * i
                if (x, y) in hits:
                    hits[(x, y)] += 1
                    if hits[(x, y)] == 2:
                        overlaps += 1
                else:
                    hits[(x, y)] = 1

    return overlaps


with open('input-files/day5.txt') as f:
    raw_input = f.read().splitlines()

line_list = parse_input(raw_input)

horizontal_and_vertical_overlaps = find_horizontal_and_vertical_overlaps(line_list)
print("Problem 1: " + str(horizontal_and_vertical_overlaps))

overlaps = find_overlaps(line_list)
print("Problem 2: " + str(overlaps))
