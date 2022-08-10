import numpy
import numpy as np


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


def count_matches(first_scanner, second_scanner, translation):
    count = 0
    second_scanner_translated = []

    # print(first_scanner)
    # print(second_scanner)

    for reading_number in range(0, len(second_scanner)):
        reading_translated = second_scanner[reading_number] + translation
        second_scanner_translated.append(reading_translated)

    # print(second_scanner_translated)

    for first_reading in first_scanner:
        for second_reading_translated in second_scanner_translated:
            if np.array_equal(first_reading, second_reading_translated):
                count += 1
    return count


def find_overlap(first_scanner, second_scanner):
    for first_reading in first_scanner:
        for second_reading in second_scanner:
            translation = [first_reading[i] - second_reading[i] for i in range(0, len(first_reading))]
            translation2 = first_reading - second_reading
            print(f"translation: {translation2}")
            count = count_matches(first_scanner, second_scanner, translation)
            print(count)
        print("")


def main():
    readings = read_file('input-files/day19_test_2d_no_rotation.txt')
    print(f"all readings: {readings}")
    find_overlap(readings[0], readings[1])


if __name__ == "__main__":
    main()
