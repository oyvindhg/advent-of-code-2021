from collections import defaultdict
from dataclasses import dataclass
from typing import List


@dataclass
class PathData:
    previous_steps: List[str]
    current_position: str


with open('input-files/day12.txt') as f:
    input_paths = f.read().splitlines()

paths = defaultdict(list)
for input_path in input_paths:
    path_pair = input_path.split('-')
    paths[path_pair[0]].append(path_pair[1])
    paths[path_pair[1]].append(path_pair[0])

path_counts = 0
path_stack = [PathData([], "start")]

while len(path_stack) > 0:
    current_path = path_stack.pop()
    previous_steps = current_path.previous_steps
    current_position = current_path.current_position
    for next_option in paths[current_position]:
        if next_option == "end":
            path_counts += 1
        elif not (next_option.islower() and next_option in previous_steps):
            new_previous_steps = list(previous_steps)
            new_previous_steps.append(current_position)
            path_stack.append(PathData(new_previous_steps, next_option))

print(path_counts)
