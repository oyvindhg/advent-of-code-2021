import dataclasses
from dataclasses import dataclass


@dataclass
class Cube:
    x_min: int
    x_max: int
    y_min: int
    y_max: int
    z_min: int
    z_max: int


@dataclass
class Instruction:
    is_on: bool
    cube: Cube


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
                cube=Cube(
                    x_min=int(x[0]),
                    x_max=int(x[1]) if len(x) > 1 else int(x[0]),
                    y_min=int(y[0]),
                    y_max=int(y[1]) if len(y) > 1 else int(y[0]),
                    z_min=int(z[0]),
                    z_max=int(z[1]) if len(z) > 1 else int(z[0]),
                )
            )
        )
    return instructions


def initialize(instructions):
    lower_bound = -50
    upper_bound = 50
    turned_on_points = set()

    for instruction in instructions:
        cube = instruction.cube
        for x in range(max(cube.x_min, lower_bound), min(cube.x_max, upper_bound) + 1):
            for y in range(max(cube.y_min, lower_bound), min(cube.y_max, upper_bound) + 1):
                for z in range(max(cube.z_min, lower_bound), min(cube.z_max, upper_bound) + 1):
                    point = (x, y, z)
                    if instruction.is_on:
                        turned_on_points.add(point)
                    else:
                        turned_on_points.discard(point)
    return turned_on_points


def split_cube(cube, void):
    """ If the areas overlap, remove the void from the cube by splitting the cube into at most six new cubes """

    overlap = Cube(
        x_min=max(cube.x_min, void.x_min),
        x_max=min(cube.x_max, void.x_max),
        y_min=max(cube.y_min, void.y_min),
        y_max=min(cube.y_max, void.y_max),
        z_min=max(cube.z_min, void.z_min),
        z_max=min(cube.z_max, void.z_max)
    )

    if overlap.x_min > overlap.x_max or (overlap.y_min > overlap.y_max) or (overlap.z_min > overlap.z_max):
        return [cube]  # There is no overlap, so just return the original cube

    splits = []

    if overlap.z_max < cube.z_max:
        # Get the whole part of the cube above the void
        top = dataclasses.replace(cube)
        top.z_min = overlap.z_max + 1
        splits.append(top)

    if overlap.z_min > cube.z_min:
        # Get the whole part of the cube below the void
        bottom = dataclasses.replace(cube)
        bottom.z_max = overlap.z_min - 1
        splits.append(bottom)

    if overlap.y_max < cube.y_max:
        # Get the part of the cube in front of the void but within the void height (z) limits
        front = dataclasses.replace(cube)
        front.y_min = overlap.y_max + 1
        front.z_min = overlap.z_min
        front.z_max = overlap.z_max
        splits.append(front)

    if overlap.y_min > cube.y_min:
        # Get the part of the cube behind of the void but within the void height (z) limits
        behind = dataclasses.replace(cube)
        behind.y_max = overlap.y_min - 1
        behind.z_min = overlap.z_min
        behind.z_max = overlap.z_max
        splits.append(behind)

    if overlap.x_max < cube.x_max:
        # Get the part of the cube to the right of the void but within the void height and front/behind (z and y) limits
        right = dataclasses.replace(overlap)
        right.x_min = overlap.x_max + 1
        right.x_max = cube.x_max
        splits.append(right)

    if overlap.x_min > cube.x_min:
        # Get the part of the cube to the left of the void but within the void height and front/behind (z and y) limits
        left = dataclasses.replace(overlap)
        left.x_max = overlap.x_min - 1
        left.x_min = cube.x_min
        splits.append(left)

    return splits


def get_volume(cube):
    return (1 + cube.x_max - cube.x_min) * (1 + cube.y_max - cube.y_min) * (1 + cube.z_max - cube.z_min)


def reboot(instructions):
    turned_on_cubes = []

    for instruction in instructions:
        new_cube = instruction.cube
        updated_turned_on_cubes = []

        for cube in turned_on_cubes:
            cubes = split_cube(cube, new_cube)
            updated_turned_on_cubes.extend(cubes)
        if instruction.is_on:
            updated_turned_on_cubes.append(new_cube)

        turned_on_cubes = updated_turned_on_cubes

    return turned_on_cubes


def main():
    instructions = read_file('input-files/day22.txt')
    turned_on_points = initialize(instructions)
    print(f"Problem 1: {len(turned_on_points)}")

    turned_on_cubes = reboot(instructions)
    print(f"Problem 2: {sum([get_volume(cube) for cube in turned_on_cubes])}")


if __name__ == "__main__":
    main()
