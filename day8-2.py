from dataclasses import dataclass
from typing import List
import numpy as np


@dataclass
class SignalEntry:
    input: List[str]
    output: List[str]


def parse_input(file_input):
    signal_entries = []
    for entries in file_input:
        patterns, out = entries.split('|')
        signal_entries.append(SignalEntry(patterns.split(), out.split()))
    return signal_entries


def count_character_occurrences(main, sub):
    occurrences = 0
    for char in sub:
        if char in main:
            occurrences += 1
    return occurrences


with open('input-files/day8.txt') as f:
    raw_input = f.read().splitlines()

signals = parse_input(raw_input)

display_number = np.empty(10, dtype=object)

outputs = []
for signal in signals:
    for signal_in in signal.input:
        signal_sorted = sorted(signal_in)
        length = len(signal_sorted)
        if length == 2:
            display_number[1] = signal_sorted
        elif length == 3:
            display_number[7] = signal_sorted
        elif length == 4:
            display_number[4] = signal_sorted
        elif length == 7:
            display_number[8] = signal_sorted

    for signal_in in signal.input:
        signal_sorted = sorted(signal_in)
        length = len(signal_sorted)
        if length == 5:
            if count_character_occurrences(signal_sorted, display_number[1]) == 2:
                display_number[3] = signal_sorted
            elif count_character_occurrences(signal_sorted, display_number[4]) == 3:
                display_number[5] = signal_sorted
            else:
                display_number[2] = signal_sorted
        elif length == 6:
            if count_character_occurrences(signal_sorted, display_number[4]) == 4:
                display_number[9] = signal_sorted
            elif count_character_occurrences(signal_sorted, display_number[1]) == 2:
                display_number[0] = signal_sorted
            else:
                display_number[6] = signal_sorted

    output = 0
    for i, signal_out in enumerate(signal.output):
        signal_sorted = sorted(signal_out)
        for j in range(10):
            if display_number[j] == signal_sorted:
                output += j * pow(10, 3 - i)
    outputs.append(output)

print(sum(outputs))
