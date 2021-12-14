from collections import defaultdict


def parse_input(file_input):
    file_template = ""
    file_rules = dict()
    for line_num, line in enumerate(file_input):
        if line:
            if line_num == 0:
                file_template = line
            else:
                file_rule = line.split(' -> ')
                file_rules[file_rule[0]] = file_rule[1]

    return file_template, file_rules


with open('input-files/day14.txt') as f:
    raw_input = f.read().splitlines()

template, rules = parse_input(raw_input)

letter_counts = defaultdict(int)
letter_pair_counts = defaultdict(int)

for i in range(0, len(template)):
    letter_counts[template[i]] += 1
    if i > 0:
        letter_pair = template[i - 1] + template[i]
        letter_pair_counts[letter_pair] += 1

for step in range(40):
    new_letter_pair_counts = defaultdict(int)
    for letter_pair in letter_pair_counts:
        count = letter_pair_counts[letter_pair]
        new_letter = rules[letter_pair]
        letter_counts[new_letter] += count

        first_pair = letter_pair[0] + new_letter
        second_pair = new_letter + letter_pair[1]
        new_letter_pair_counts[first_pair] += count
        new_letter_pair_counts[second_pair] += count

    letter_pair_counts = new_letter_pair_counts

a = sorted(letter_counts.values())
print(a[-1] - a[0])
