import numpy as np
from dataclasses import dataclass
from typing import List

hex_to_binary_table = {
    '0': "0000",
    '1': "0001",
    '2': "0010",
    '3': "0011",
    '4': "0100",
    '5': "0101",
    '6': "0110",
    '7': "0111",
    '8': "1000",
    '9': "1001",
    'A': "1010",
    'B': "1011",
    'C': "1100",
    'D': "1101",
    'E': "1110",
    'F': "1111"
}

Version, Literal, Operator, End = range(4)

Sum, Product, Minimum, Maximum, Noop, Greater, Less, Equal = range(8)


@dataclass
class Operator:
    current_position: int
    length_type: int
    length: int
    values: List[int]
    operation: int


def binary_to_num(binary_string):
    number = 0
    string_length = len(binary_string)
    for i, digit in enumerate(binary_string):
        if int(digit) == 1:
            number += 2 ** (string_length - i - 1)
    return number


def hex_to_binary(hex_text):
    binary_text = ""
    for letter in hex_text:
        binary_text += hex_to_binary_table[letter]
    return binary_text


def apply_operation(values, operation):
    if operation == Sum:
        return sum(values)
    elif operation == Product:
        return np.prod(values)
    elif operation == Minimum:
        return min(values)
    elif operation == Maximum:
        return max(values)
    elif operation == Greater:
        return values[0] > values[1]
    elif operation == Less:
        return values[0] < values[1]
    elif operation == Equal:
        return values[0] == values[1]
    else:
        raise ValueError("Operation not recognized", operation)


with open('input-files/day16.txt') as f:
    raw_input = f.read()

binary_input = hex_to_binary(raw_input)

binary_input_length = len(binary_input)

current_position = 0
expected_type = Version
packet_stack = []
type_id = 0
literal_value_binary = ""

version_number_sum = 0
outer_packet_value = 0

while expected_type != End:
    if expected_type == Version:
        version_number_binary = binary_input[current_position:current_position + 3]
        version_number = binary_to_num(version_number_binary)

        version_number_sum += version_number

        type_id_binary = binary_input[current_position + 3:current_position + 6]
        type_id = binary_to_num(type_id_binary)

        current_position += 6

        if type_id == 4:
            expected_type = Literal
        else:
            expected_type = Operator

    elif expected_type == Literal:
        literal_prefix = binary_input[current_position]
        literal_value_binary += binary_input[current_position + 1: current_position + 5]

        current_position += 5

        if literal_prefix == '0':
            literal_value = binary_to_num(literal_value_binary)
            literal_value_binary = ""

            value = literal_value
            update_packets = True
            while update_packets and packet_stack:
                packet = packet_stack[-1]
                packet.values.append(value)
                if packet.length_type == 0:
                    length = packet.length - (current_position - packet.current_position)
                else:
                    length = packet.length - 1

                if length == 0:
                    value = apply_operation(packet.values, packet.operation)
                    packet_stack.pop()
                    if not packet_stack:
                        outer_packet_value = value
                else:
                    packet.length = length
                    packet.current_position = current_position
                    update_packets = False

            if packet_stack:
                expected_type = Version
            else:
                expected_type = End

    elif expected_type == Operator:
        packet_length_prefix = binary_input[current_position]

        if packet_length_prefix == '0':
            packet_length_binary = binary_input[current_position + 1: current_position + 16]
            packet_length = binary_to_num(packet_length_binary)

            current_position += 16
            packet_stack.append(
                Operator(
                    current_position=current_position,
                    length_type=0,
                    length=packet_length,
                    values=[],
                    operation=type_id
                )
            )
            expected_type = Version
        else:
            packet_length_binary = binary_input[current_position + 1: current_position + 12]
            packet_length = binary_to_num(packet_length_binary)

            current_position += 12
            packet_stack.append(
                Operator(
                    current_position=current_position,
                    length_type=1,
                    length=packet_length,
                    values=[],
                    operation=type_id
                )
            )
            expected_type = Version
    else:
        raise ValueError("Type not recognized", expected_type)

print(f"Problem 1: {version_number_sum}")
print(f"Problem 2: {outer_packet_value}")
