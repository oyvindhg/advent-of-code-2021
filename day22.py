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
        is_on, box = row.split(' ')
        x_raw, y_raw, z_raw = box.split(',')
        x = x_raw.split('x=')[1].split('..')
        y = y_raw.split('y=')[1].split('..')
        z = z_raw.split('z=')[1].split('..')
        instructions.append(
            Instruction(
                is_on=bool(is_on),
                x_min=int(x[0]),
                x_max=int(x[1]) if len(x) > 1 else int(x[0]),
                y_min=int(y[0]),
                y_max=int(y[1]) if len(y) > 1 else int(y[0]),
                z_min=int(z[0]),
                z_max=int(z[1]) if len(z) > 1 else int(z[0]),
            )
        )
    return instructions


def main():
    instructions = read_file('input-files/day22_test.txt')
    print(instructions)


if __name__ == "__main__":
    main()
