with open('input-files/day6.txt') as f:
    initial_fish = list(map(int, f.read().split(',')))

fish_age_counts = [0] * 9
for fish in initial_fish:
    fish_age_counts[fish] += 1

for day in range(80):
    new_fish = fish_age_counts[0]
    for i in range(0, 8):
        fish_age_counts[i] = fish_age_counts[i + 1]
    fish_age_counts[6] += new_fish
    fish_age_counts[8] = new_fish

print("Problem 1: " + str(sum(fish_age_counts)))

for day in range(80, 256):
    new_fish = fish_age_counts[0]
    for i in range(0, 8):
        fish_age_counts[i] = fish_age_counts[i + 1]
    fish_age_counts[6] += new_fish
    fish_age_counts[8] = new_fish

print("Problem 2: " + str(sum(fish_age_counts)))
