from __future__ import annotations

import copy
import math
import re


class Pair:
    left: any = None
    right: any = None
    parent: Pair = None

    def __str__(self):
        return "[" + str(self.left) + ", " + str(self.right) + "]"


def parse_snail_number(text):
    current = None
    first = current

    # Split on '[', ']' and ','
    split_text = re.split(r'(\[|]|,)', text)

    for chars in split_text:
        if chars == '[':
            parent = current
            current = Pair()
            current.parent = parent
            if parent is None:
                first = current
            else:
                if parent.left is None:
                    parent.left = current
                else:
                    parent.right = current
        elif chars.isnumeric():
            if current.left is None:
                current.left = int(chars)
            else:
                current.right = int(chars)
        elif chars == ']':
            current = current.parent
        elif chars == ',' or chars == '':
            pass
        else:
            raise ValueError("Characters not recognized", chars)
    return first


def add(a: Pair, b: Pair):
    parent = Pair()
    parent.left = a
    parent.right = b
    a.parent = parent
    b.parent = parent
    return parent


def explode(pair: Pair):
    visited = []
    current = pair
    depth = 1
    prev = None
    left, right = range(2)
    prev_dir = None
    exploded = False
    exploded_right = 0

    while current or visited:
        while current:
            visited.append((current, depth))
            if isinstance(current.left, Pair):
                depth += 1
                if depth == 5 and not exploded:
                    exploded_right = current.left.right
                    if prev is not None:
                        if prev_dir == left:
                            prev.left += current.left.left
                        else:
                            prev.right += current.left.left
                    current.left = 0
                    exploded = True
                    current = None
                else:
                    current = current.left
            else:
                if exploded:
                    current.left += exploded_right
                    return True
                prev = current
                prev_dir = left
                current = None
        current, depth = visited.pop()
        if isinstance(current.right, Pair):
            depth += 1
            if depth == 5 and not exploded:
                exploded_right = current.right.right
                if prev is not None:
                    if prev_dir == left:
                        prev.left += current.right.left
                    else:
                        prev.right += current.right.left
                current.right = 0
                exploded = True
                current = None
            else:
                current = current.right
        else:
            if exploded:
                current.right += exploded_right
                return True
            prev = current
            prev_dir = right
            current = None

    return exploded


def split(pair: Pair):
    visited = []
    current = pair

    while current or visited:
        while current:
            visited.append(current)
            if isinstance(current.left, Pair):
                current = current.left
            else:
                value = current.left
                if value > 9:
                    new_pair = Pair()
                    new_pair.left = math.floor(value / 2)
                    new_pair.right = math.ceil(value / 2)
                    current.left = new_pair
                    return True
                current = None
        current = visited.pop()
        if isinstance(current.right, Pair):
            current = current.right
        else:
            value = current.right
            if value > 9:
                new_pair = Pair()
                new_pair.left = math.floor(value / 2)
                new_pair.right = math.ceil(value / 2)
                current.right = new_pair
                return True
            current = None

    return False


def find_magnitude(pair: Pair):
    visited = []
    current = pair
    multiplier = 1
    magnitude = 0

    while current or visited:
        while current:
            visited.append((current, multiplier))
            if isinstance(current.left, Pair):
                multiplier *= 3
                current = current.left
            else:
                multiplier *= 3
                magnitude += multiplier * current.left
                current = None
        current, multiplier = visited.pop()
        if isinstance(current.right, Pair):
            multiplier *= 2
            current = current.right
        else:
            multiplier *= 2
            magnitude += multiplier * current.right
            current = None

    return magnitude


with open('input-files/day18.txt') as f:
    pairs = [parse_snail_number(row) for row in f.read().splitlines()]

copied_pairs = copy.deepcopy(pairs)
pair = copied_pairs[0]
for i in range(1, len(copied_pairs)):
    pair = add(pair, copied_pairs[i])

    exploded = True
    is_split = True
    while exploded or is_split:
        exploded = explode(pair)
        if not exploded:
            is_split = split(pair)

print(f"Problem 1: {find_magnitude(pair)}")

max_magnitude = 0
for i in range(0, len(pairs)):
    for j in range(0, len(pairs)):
        if i != j:
            pairs_i = copy.deepcopy(pairs[i])
            pairs_j = copy.deepcopy(pairs[j])
            pair = add(pairs_i, pairs_j)
            exploded = True
            is_split = True
            while exploded or is_split:
                exploded = explode(pair)
                if not exploded:
                    is_split = split(pair)
            magnitude = find_magnitude(pair)
            max_magnitude = max(magnitude, max_magnitude)

print(f"Problem 2: {max_magnitude}")
