from dataclasses import dataclass

import numpy as np


@dataclass
class Transformation:
    start: int
    end: int
    rotation: np.array
    translation: np.array


rotation_matrices = np.array([
    [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
    [[1, 0, 0], [0, 0, -1], [0, 1, 0]],
    [[1, 0, 0], [0, -1, 0], [0, 0, -1]],
    [[1, 0, 0], [0, 0, 1], [0, -1, 0]],

    [[0, -1, 0], [1, 0, 0], [0, 0, 1]],
    [[0, 0, 1], [1, 0, 0], [0, 1, 0]],
    [[0, 1, 0], [1, 0, 0], [0, 0, -1]],
    [[0, 0, -1], [1, 0, 0], [0, -1, 0]],

    [[-1, 0, 0], [0, -1, 0], [0, 0, 1]],
    [[-1, 0, 0], [0, 0, -1], [0, -1, 0]],
    [[-1, 0, 0], [0, 1, 0], [0, 0, -1]],
    [[-1, 0, 0], [0, 0, 1], [0, 1, 0]],

    [[0, 1, 0], [-1, 0, 0], [0, 0, 1]],
    [[0, 0, 1], [-1, 0, 0], [0, -1, 0]],
    [[0, -1, 0], [-1, 0, 0], [0, 0, -1]],
    [[0, 0, -1], [-1, 0, 0], [0, 1, 0]],

    [[0, 0, -1], [0, 1, 0], [1, 0, 0]],
    [[0, 1, 0], [0, 0, 1], [1, 0, 0]],
    [[0, 0, 1], [0, -1, 0], [1, 0, 0]],
    [[0, 0, -1], [0, -1, 0], [1, 0, 0]],

    [[0, 0, -1], [0, -1, 0], [-1, 0, 0]],
    [[0, -1, 0], [0, 0, 1], [-1, 0, 0]],
    [[0, 0, 1], [0, 1, 0], [-1, 0, 0]],
    [[0, 1, 0], [0, 0, -1], [-1, 0, 0]],
])


def read_file(filepath):
    readings = []
    current_readings = []
    with open(filepath) as f:
        rows = f.read().splitlines()
    for row in rows:
        if row.startswith("---"):
            current_readings = []
        elif not row:
            readings.append(current_readings)
        else:
            numbers = np.array([int(number) for number in row.split(',')])
            current_readings.append(numbers)
    readings.append(current_readings)
    return readings


def count_matches(first_scanner, second_scanner, rotation, translation):
    count = 0
    second_scanner_translated = []

    for reading_number in range(0, len(second_scanner)):
        reading_translated = rotation.dot(second_scanner[reading_number]) + translation
        second_scanner_translated.append(reading_translated)

    for first_reading in first_scanner:
        for second_reading_translated in second_scanner_translated:
            if np.array_equal(first_reading, second_reading_translated):
                count += 1
    return count


def find_transformation(first_scanner, second_scanner):
    transformation_counter = dict()
    for rotation_num, rotation in enumerate(rotation_matrices):
        for first_reading in first_scanner:
            for second_reading in second_scanner:
                second_reading_rotated = rotation.dot(second_reading)
                translation = first_reading - second_reading_rotated

                transform_id = (rotation_num, translation[0], translation[1], translation[2])
                transformation_counter[transform_id] = transformation_counter.get(transform_id, 0) + 1

                if transformation_counter[transform_id] >= 12:
                    return rotation, translation
    return None, None


def find_transformations(readings):
    transformations = []
    for second in range(0, len(readings)):
        for first in range(0, len(readings)):
            if second != 0 and second != first:
                rotation, translation = find_transformation(readings[first], readings[second])
                if rotation is not None:
                    transformations.append(
                        Transformation(start=second, end=first, rotation=rotation, translation=translation)
                    )
    return transformations


def find_transformation_paths(transformations, beacon_count):
    queue = [(0, [])]
    shortest_transformations = [[]] * beacon_count
    shortest_transformations[0] = [0]
    while any(x == [] for x in shortest_transformations):
        destination, current_path = queue.pop(0)
        next_steps = [t for t in transformations if (t.end == destination and shortest_transformations[t.start] == [])]
        for step in next_steps:
            updated_path = current_path + [step.end]
            queue.append((step.start, updated_path))
            if not shortest_transformations[step.start]:
                shortest_transformations[step.start] = updated_path
    return shortest_transformations


def count_beacons(readings):
    print("Transform")
    transformations = find_transformations(readings)
    print("Paths")
    paths = find_transformation_paths(transformations, len(readings))

    beacon_counter = 0
    beacons = set()
    print("Counter")
    for i, reading in enumerate(readings):
        if i == 0:
            for point in reading:
                beacon_counter += 1
                beacons.add((point[0], point[1], point[2]))
        else:
            path = paths[i]
            for point in reading:
                start = i
                for step in reversed(path):
                    transformation = next(t for t in transformations if (t.start == start and t.end == step))
                    point = transformation.rotation.dot(point) + transformation.translation
                    start = step
                point_id = (point[0], point[1], point[2])
                if point_id not in beacons:
                    beacon_counter += 1
                    beacons.add(point_id)
    return beacon_counter


def main():
    readings = read_file('input-files/day19.txt')
    count = count_beacons(readings)

    print(f"Problem 1: {count}")


if __name__ == "__main__":
    main()
