def read_file(filepath):
    with open(filepath) as f:
        instructions = f.read().splitlines()
    return instructions


def find_model_number(incomplete_model_number, instructions):
    variables = {'w': 0, 'x': 0, 'y': 0, 'z': 0}
    number_index = 0
    model_number = ""

    for instruction in instructions:
        instruction_list = instruction.split()
        operation = instruction_list[0]
        variable = instruction_list[1]
        if operation == 'inp':
            digit = incomplete_model_number[number_index]
            variables[variable] = digit
            if digit != '?':
                model_number += digit
                variables[variable] = int(variables.get(variable))
            number_index += 1
        else:
            value = instruction_list[2]
            if value in ['w', 'x', 'y', 'z']:
                value = variables[value]
            else:
                value = int(value)
            if operation == 'add':
                variables[variable] += value
            elif operation == 'mul':
                variables[variable] *= value
            elif operation == 'div':
                variables[variable] = int(variables.get(variable) / value)
            elif operation == 'mod':
                variables[variable] %= value
            elif operation == 'eql':
                if variable == 'x' and value == '?':  # This operation checks if x == w
                    value = variables['x']
                    if 1 <= value <= 9:
                        model_number += str(value)
                        variables['w'] = value
                    else:
                        return None
                variables[variable] = 1 if variables[variable] == value else 0
            else:
                raise RuntimeError("Invalid operation")

    return model_number


def create_incomplete_model_number(numbers):
    return numbers[0:4] + '?' + numbers[4:6] + '?' + numbers[6] + '?????'


def find_max_model_number(instructions):
    numbers = "9999999"
    while True:
        if '0' not in numbers:
            incomplete_model_number = create_incomplete_model_number(numbers)
            model_number = find_model_number(incomplete_model_number, instructions)
            if model_number is not None:
                return model_number
        numbers = str(int(numbers) - 1)


def find_min_model_number(instructions):
    numbers = "1111111"
    while True:
        if '0' not in numbers:
            incomplete_model_number = create_incomplete_model_number(numbers)
            model_number = find_model_number(incomplete_model_number, instructions)
            if model_number is not None:
                return model_number
        numbers = str(int(numbers) + 1)


def main():
    instructions = read_file('input-files/day24.txt')

    max_model_number = find_max_model_number(instructions)
    print(f"Problem 1: {max_model_number}")

    min_model_number = find_min_model_number(instructions)
    print(f"Problem 2: {min_model_number}")


if __name__ == "__main__":
    main()
