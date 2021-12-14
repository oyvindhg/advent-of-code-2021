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

for letter in template:
    letter_counts[letter] += 1

for step in range(10):
    template_length = len(template)
    new_template = template[0]
    for i in range(1, template_length):
        letter_pair = template[i - 1:i + 1]
        new_letter = rules[letter_pair]
        letter_counts[new_letter] += 1
        new_template += new_letter + letter_pair[1]
    template = new_template

a = sorted(letter_counts.values())
print(a[-1] - a[0])
