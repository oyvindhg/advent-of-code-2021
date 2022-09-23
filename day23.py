import copy
import math
from dataclasses import dataclass


@dataclass
class Amphipod:
    type: chr
    position_type: chr
    position: int
    visited_hallway: bool
    finished: bool


def read_file(filepath):
    with open(filepath) as f:
        rows = f.read().splitlines()
        amphipods = []
        position_types = ['A', 'B', 'C', 'D']
        amphipod_number = 0
        for row in rows:
            for letter in row:
                if letter == 'A' or letter == 'B' or letter == 'C' or letter == 'D':
                    position_type = position_types[amphipod_number % len(position_types)]
                    position = int(amphipod_number / len(position_types))

                    amphipods.append(
                        Amphipod(
                            type=letter,
                            position_type=position_type,
                            position=position,
                            visited_hallway=False,
                            finished=False
                        )
                    )
                    amphipod_number += 1

        for amphipod in amphipods:
            if amphipod.type == amphipod.position_type:
                other_type_amphipods_behind = [a for a in amphipods if
                                               a.position_type == amphipod.position_type and
                                               a.position > amphipod.position and
                                               a.type != amphipod.type]

                if not other_type_amphipods_behind:
                    amphipod.finished = True

    room_depth = int(amphipod_number / len(position_types))

    return amphipods, room_depth


def display(amphipods, room_depth):
    p = {}
    for a in amphipods:
        p[a.position_type + str(a.position)] = a.type

    hallway = ""
    for i in range(0, 11):
        position = 'H' + str(i)
        hallway += p.get(position, '.')

    string = f"""
    #############
    #{hallway}#
    ###{p.get('A0', '.')}#{p.get('B0', '.')}#{p.get('C0', '.')}#{p.get('D0', '.')}###
    """
    for i in range(1, room_depth):
        string += f"  #{p.get('A' + str(i), '.')}#{p.get('B' + str(i), '.')}#{p.get('C' + str(i), '.')}#{p.get('D' + str(i), '.')}#\n"
    string += "      #########\n"
    print(string)


def search_shortest_path(initial_amphipods, room_depth):
    possible_hallway_stops = [0, 1, 3, 5, 7, 9, 10]
    hallway_exits = {'A': 2, 'B': 4, 'C': 6, 'D': 8}
    step_weight = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}

    queue = [(initial_amphipods, 0, "")]
    min_path_energy = math.inf
    best_path = ""

    visited_states = {}

    while queue:
        amphipods, current_energy, path = queue.pop()
        # display(amphipods, room_depth)

        positions = {}
        for a in amphipods:
            positions[a.position_type + str(a.position)] = a.type

        state_id = ""
        for i in range(0, 11):
            position = 'H' + str(i)
            state_id += positions.get(position, '.')
        for i in range(0, room_depth):
            state_id += positions.get('A' + str(i), '.') + positions.get('B' + str(i), '.') + \
                        positions.get('C' + str(i), '.') + positions.get('D' + str(i), '.')

        skip_state = False
        if state_id in visited_states:
            if current_energy < visited_states.get(state_id):
                visited_states[state_id] = current_energy
            else:
                skip_state = True
        else:
            visited_states[state_id] = current_energy

        if not skip_state:
            for a_num, a in enumerate(amphipods):
                if not a.finished:
                    if not a.visited_hallway:
                        hallway_exit = hallway_exits.get(a.position_type)
                        for stop in possible_hallway_stops:

                            no_blockers = True
                            for i in range(0, a.position):
                                if a.position_type + str(i) in positions:
                                    no_blockers = False
                            for i in range(min(hallway_exit, stop), max(hallway_exit, stop) + 1):
                                if 'H' + str(i) in positions:
                                    no_blockers = False

                            if no_blockers:
                                updated_amphipods = copy.deepcopy(amphipods)
                                updated_amphipods[a_num].position_type = 'H'
                                updated_amphipods[a_num].position = stop
                                updated_amphipods[a_num].visited_hallway = True
                                updated_energy = current_energy + (a.position + 1 + abs(stop - hallway_exit)) * step_weight.get(a.type)
                                updated_path = path + f"{a.position_type}{a.position} -> H{stop} "

                                if updated_energy < min_path_energy:
                                    queue.append((updated_amphipods, updated_energy, updated_path))

                    else:
                        hallway_exit = hallway_exits.get(a.type)
                        is_room_ready = True
                        is_empty_position = False
                        position = room_depth - 1
                        while position >= 0 and not is_empty_position and is_room_ready:
                            position_id = a.type + str(position)
                            if position_id in positions:
                                if positions.get(position_id) != a.type:
                                    is_room_ready = False
                                else:
                                    position -= 1
                            else:
                                is_empty_position = True

                        if is_room_ready and is_empty_position:
                            is_room_right = hallway_exit > a.position

                            no_blockers = True
                            if is_room_right:
                                for i in range(a.position + 1, hallway_exit + 1):
                                    if 'H' + str(i) in positions:
                                        no_blockers = False
                            else:
                                for i in range(hallway_exit, a.position):
                                    if 'H' + str(i) in positions:
                                        no_blockers = False

                            if no_blockers:
                                updated_amphipods = copy.deepcopy(amphipods)
                                updated_amphipods[a_num].position_type = a.type
                                updated_amphipods[a_num].position = position
                                updated_amphipods[a_num].finished = True
                                updated_energy = current_energy + (position + 1 + abs(a.position - hallway_exit)) * step_weight.get(a.type)
                                updated_path = path + f"H{a.position} -> {a.type}{position} "

                                if updated_energy < min_path_energy:
                                    if not any(not b.finished for b in updated_amphipods):
                                        min_path_energy = updated_energy
                                        best_path = updated_path
                                    else:
                                        queue.append((updated_amphipods, updated_energy, updated_path))

    return min_path_energy, best_path


def main():
    amphipods, room_depth = read_file('input-files/day23_part_1.txt')
    energy, best_path = search_shortest_path(amphipods, room_depth)
    print(f"Problem 1: {energy} (best path: {best_path})")

    amphipods, room_depth = read_file('input-files/day23_part_2.txt')
    energy, best_path = search_shortest_path(amphipods, room_depth)
    print(f"Problem 2: {energy} (best path: {best_path})")


if __name__ == "__main__":
    main()
