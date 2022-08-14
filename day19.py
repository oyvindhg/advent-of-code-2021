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


def find_scanners_and_beacons(readings):
    transformations = find_transformations(readings)
    paths = find_transformation_paths(transformations, len(readings))
    beacons = set()
    scanners = []
    for i, reading in enumerate(readings):
        if i == 0:
            # Add scanner location
            scanners.append((0, 0, 0))

            # Add beacon locations
            for point in reading:
                beacons.add((point[0], point[1], point[2]))
        else:
            path = paths[i]
            # Find and add scanner location
            start = i
            point = np.array([0, 0, 0])
            for step in reversed(path):
                transformation = next(t for t in transformations if (t.start == start and t.end == step))
                point = transformation.rotation.dot(point) + transformation.translation
                start = step
            scanners.append((point[0], point[1], point[2]))

            # Find and add new beacon locations
            for point in reading:
                start = i
                for step in reversed(path):
                    transformation = next(t for t in transformations if (t.start == start and t.end == step))
                    point = transformation.rotation.dot(point) + transformation.translation
                    start = step
                point_id = (point[0], point[1], point[2])
                if point_id not in beacons:
                    beacons.add(point_id)

    return scanners, list(beacons)


def find_distance(first_scanner, second_scanner):
    return abs(first_scanner[0] - second_scanner[0]) + \
           abs(first_scanner[1] - second_scanner[1]) + \
           abs(first_scanner[2] - second_scanner[2])


def find_max_distance(scanners):
    max_distance = 0
    for first in range(0, len(scanners)):
        for second in range(0, first):
            distance = find_distance(scanners[first], scanners[second])
            if distance > max_distance:
                max_distance = distance
    return max_distance


def main():
    readings = read_file('input-files/day19.txt')
    scanners, beacons = find_scanners_and_beacons(readings)

    beacon_count = len(beacons)
    print(f"Problem 1: {beacon_count}")

    max_distance = find_max_distance(scanners)
    print(f"Problem 2: {max_distance}")


if __name__ == "__main__":
    main()
