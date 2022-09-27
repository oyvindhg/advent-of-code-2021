def read_file(filepath):
    with open(filepath) as f:
        rows = f.read().splitlines()
    width = len(rows[0])
    length = len(rows)
    sea_cucumbers = {}
    for r, row in enumerate(rows):
        for c, character in enumerate(row):
            if character != '.':
                sea_cucumbers[(r, c)] = character
    return sea_cucumbers, width, length


def display(sea_cucumbers, width, length):
    sea_cucumber_string = ""
    for r in range(0, length):
        for c in range(0, width):
            character = sea_cucumbers.get((r, c))
            if character is not None:
                sea_cucumber_string += character
            else:
                sea_cucumber_string += '.'
        sea_cucumber_string += '\n'
    print(sea_cucumber_string)


def perform_step(sea_cucumbers, width, length):
    # print(f"first: {sea_cucumbers}")
    updated_sea_cucumbers = {}
    has_movement = False
    for r, c in sea_cucumbers.keys():  # Horizontal sea cucumbers move
        if sea_cucumbers[(r, c)] == '>':
            next_c = (c+1) % width
            if (r, next_c) not in sea_cucumbers.keys():
                has_movement = True
                updated_sea_cucumbers[(r, next_c)] = '>'
            else:
                updated_sea_cucumbers[(r, c)] = '>'

    for r, c in sea_cucumbers.keys():  # Vertical sea cucumbers move
        if sea_cucumbers[(r, c)] == 'v':
            next_r = (r+1) % length
            if (next_r, c) not in updated_sea_cucumbers.keys() and sea_cucumbers.get((next_r, c)) != 'v':
                has_movement = True
                updated_sea_cucumbers[(next_r, c)] = 'v'
            else:
                updated_sea_cucumbers[(r, c)] = 'v'

    # print(f"after: {updated_sea_cucumbers}")
    return updated_sea_cucumbers, has_movement


def find_step_number(sea_cucumbers, width, length):
    step_number = 1
    while True:
        sea_cucumbers, has_movement = perform_step(sea_cucumbers, width, length)
        if not has_movement:
            # display(sea_cucumbers, width, length)
            return step_number
        step_number += 1


def main():
    sea_cucumbers, width, length = read_file('input-files/day25.txt')

    step_number = find_step_number(sea_cucumbers, width, length)
    print(f"Problem 1: {step_number}")


if __name__ == "__main__":
    main()
