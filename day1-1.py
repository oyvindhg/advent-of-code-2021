with open('input-files/day1.txt') as f:
    points = [int(point) for point in f.read().splitlines()]

increase_count = 0
for i in range(1, len(points)):
    if points[i] > points[i-1]:
        increase_count += 1

print(increase_count)
