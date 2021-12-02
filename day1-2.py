with open('input-files/day1.txt') as f:
    points = [int(point) for point in f.read().splitlines()]

increase_count = 0
for i in range(3, len(points)):
    current_window = sum(points[i-2:i+1])
    previous_window = sum(points[i-3:i])

    if current_window > previous_window:
        increase_count += 1

print(increase_count)
