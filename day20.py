import numpy as np


def read_file(filepath):
    with open(filepath) as f:
        rows = f.read().splitlines()
    algorithm = ""
    image = ""
    for i, row in enumerate(rows):
        if i == 0:
            algorithm = row
        elif row:
            image += row + '\n'
    return algorithm, image


def initialize_image(raw_image):
    rows = raw_image.split('\n')[:-1]
    width = len(rows[0])
    height = len(rows)

    image = np.array([['?'] * width] * height)
    for r, row in enumerate(rows):
        for c, sign in enumerate(row):
            image[r][c] = sign
    image = np.pad(image, pad_width=1, constant_values='.')  # Pad with dark pixels
    image = np.pad(image, pad_width=1, constant_values='*')  # Pad with a symbol marking infinity
    return image


def binary_to_decimal(binary_string):
    number = 0
    binary_length = len(binary_string)
    for i, digit in enumerate(binary_string):
        if int(digit) == 1:
            number += 2 ** (binary_length - i - 1)
    return number


def enhance(image, algorithm):
    width = len(image[0])
    height = len(image)
    new_image = np.array([['?'] * width] * height)

    current_edge_pixel = image[1][1]
    infinity_index = 0 if image[1][1] == '.' else 511
    infinity_pixel = algorithm[infinity_index]
    for r in range(0, width):
        for c in range(0, height):
            if image[r][c] == '*':
                new_image[r][c] = infinity_pixel
            else:
                output_matrix = image[r-1:r+2, c-1:c+2]
                # print(output_matrix)
                output_list = output_matrix.flatten()
                pixel_index = "".join([str(char) for char in output_list])
                # print(pixel_index)
                binary_index = pixel_index.replace('*', current_edge_pixel).replace('.', '0').replace('#', '1')
                # print(binary_index)
                decimal_index = binary_to_decimal(binary_index)
                # print(decimal_index)
                pixel = algorithm[decimal_index]
                new_image[r][c] = pixel
                # print(pixel)
    # print(new_image)
    new_image = np.pad(new_image, pad_width=1, constant_values='*')  # Pad with a symbol marking infinity
    return new_image


def count_light_pixels(image):
    count = 0
    width = len(image[0])
    height = len(image)
    for r in range(0, width):
        for c in range(0, height):
            if image[r][c] == '#':
                count += 1
    return count


def main():
    algorithm, raw_image = read_file('input-files/day20.txt')
    image = initialize_image(raw_image)
    for i in range(0, 2):
        image = enhance(image, algorithm)
    count = count_light_pixels(image)
    print(f"Problem 1: {count}")

    for i in range(2, 50):
        image = enhance(image, algorithm)
    count = count_light_pixels(image)
    print(f"Problem 2: {count}")


if __name__ == "__main__":
    main()
