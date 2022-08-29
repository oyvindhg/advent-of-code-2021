from dataclasses import dataclass


@dataclass
class Instruction:
    is_on: bool
    x_min: int
    x_max: int
    y_min: int
    y_max: int
    z_min: int
    z_max: int


def read_file(filepath):
    with open(filepath) as f:
        rows = f.read().splitlines()

    instructions = []
    for row in rows:
        on_or_off, box = row.split(' ')
        x_raw, y_raw, z_raw = box.split(',')
        x = x_raw.split('x=')[1].split('..')
        y = y_raw.split('y=')[1].split('..')
        z = z_raw.split('z=')[1].split('..')
        instructions.append(
            Instruction(
                is_on=bool(on_or_off == "on"),
                x_min=int(x[0]),
                x_max=int(x[1]) if len(x) > 1 else int(x[0]),
                y_min=int(y[0]),
                y_max=int(y[1]) if len(y) > 1 else int(y[0]),
                z_min=int(z[0]),
                z_max=int(z[1]) if len(z) > 1 else int(z[0]),
            )
        )
    return instructions


def initialize(instructions):
    lower_bound = -50
    upper_bound = 50
    turned_on = set()

    for instruction in instructions:
        for x in range(max(instruction.x_min, lower_bound), min(instruction.x_max, upper_bound) + 1):
            for y in range(max(instruction.y_min, lower_bound), min(instruction.y_max, upper_bound) + 1):
                for z in range(max(instruction.z_min, lower_bound), min(instruction.z_max, upper_bound) + 1):
                    point = (x, y, z)
                    if instruction.is_on:
                        turned_on.add(point)
                    else:
                        turned_on.discard(point)
    return turned_on


def main():
    instructions = read_file('input-files/day22.txt')
    turned_on = initialize(instructions)
    print(f"Problem 1: {len(turned_on)}")


if __name__ == "__main__":
    main()
