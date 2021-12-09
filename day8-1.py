from dataclasses import dataclass

from typing import List


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


with open('input-files/day8.txt') as f:
    raw_input = f.read().splitlines()

signals = parse_input(raw_input)

unique_count = 0
for signal in signals:
    for entry in signal.output:
        length = len(entry)
        if length == 2 or length == 3 or length == 4 or length == 7:
            unique_count += 1

print(unique_count)
