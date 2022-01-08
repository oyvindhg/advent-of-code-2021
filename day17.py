import math

with open('input-files/day17.txt') as f:
    raw_input = f.read()

targets = raw_input.split(": ")[-1].split(", ")

x_values = targets[0].split('=')[-1].split("..")
x_min = int(x_values[0])
x_max = int(x_values[-1])

y_values = targets[1].split('=')[-1].split("..")
y_min = int(y_values[0])
y_max = int(y_values[-1])

print(f"Problem 1: {sum(range(-y_min))}")

vy_min = y_min
vy_max = -y_min - 1
# Using the quadratic formula to find min horizontal speed that ends up at beginning of target
vx_min = math.floor((math.sqrt(1 + 8 * x_min) - 1) / 2)
vx_max = x_max

i = 0

hits = 0
for vx_0 in range(vx_min, vx_max + 1):
    for vy_0 in range(vy_min, vy_max + 1):
        x = 0
        y = 0
        vx = vx_0
        vy = vy_0
        while x <= x_max and y >= y_min:
            x += vx
            y += vy
            vx = vx - 1 if vx > 0 else vx + 1 if vx < 0 else 0
            vy = vy - 1
            if x_min <= x <= x_max and y_min <= y <= y_max:
                hits += 1
                break

print(f"Problem 2: {hits}")
