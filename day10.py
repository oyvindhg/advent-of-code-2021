import numpy as np

with open('input-files/day10.txt') as f:
    lines = f.read().splitlines()

broken_score_table = {')': 3, ']': 57, '}': 1197, '>': 25137}

score = 0
incomplete_lines = []
for line in lines:
    stack = []
    for character in line:
        if character == '(':
            stack.append(')')
        elif character == '[':
            stack.append(']')
        elif character == '{':
            stack.append('}')
        elif character == '<':
            stack.append('>')
        else:
            expected_char = stack.pop()
            if character != expected_char:
                score += broken_score_table[character]
                break
    else:  # Will not be entered if the for loop was broken out of
        incomplete_lines.append(line)

print("Problem 1: " + str(score))

incomplete_score_table = {')': 1, ']': 2, '}': 3, '>': 4}
incomplete_scores = []
for line in incomplete_lines:
    stack = []
    for character in line:
        if character == '(':
            stack.append(')')
        elif character == '[':
            stack.append(']')
        elif character == '{':
            stack.append('}')
        elif character == '<':
            stack.append('>')
        else:
            stack.pop()
    line_score = 0
    while len(stack) > 0:
        line_score *= 5
        line_score += incomplete_score_table[stack.pop()]
    incomplete_scores.append(line_score)

sorted_scores = sorted(incomplete_scores)

print("Problem 2: " + str(int(np.median(incomplete_scores))))
