import math
from data_2019 import day_1_input, day_2_input, day_3_input, day_4_input, day_5_input, day_6_input

############### DAY 1 ###############
def calculate_simple_fuel(module):
    return math.floor(module / 3) - 2

def calculate_complex_fuel(module):
    total_fuel = 0
    fuel_req = calculate_simple_fuel(module)
    if fuel_req > 0:
        total_fuel += fuel_req + total_fuel + calculate_complex_fuel(fuel_req)
    return total_fuel

# Day 1 - Part 1
def simple_fuel_requirements(fuel_modules):
    total_fuel = 0
    for module in fuel_modules:
        total_fuel += calculate_simple_fuel(module)
    return total_fuel

# Day 1 - Part 2
def complex_fuel_requirements(fuel_modules):
    total_fuel = 0
    for module in fuel_modules:
        total_fuel += calculate_complex_fuel(module)
    return total_fuel


############### DAY 2 ###############
def process_intcode(intcode, input_integer):
    ic = intcode.copy()
    outputs = []
    i = 0
    while ic[i] != 99:
        expanded_opcode = str(ic[i]).zfill(4)
        opcode = int(expanded_opcode[-2:])
        mode1 = int(expanded_opcode[1:2])
        mode2 = int(expanded_opcode[0:1])
    
        if opcode == 1:
            param1 = ic[ic[i + 1]] if mode1 == 0 else ic[i + 1]
            param2 = ic[ic[i + 2]] if mode2 == 0 else ic[i + 2]
            result_pos = ic[i + 3]
            ic[result_pos] = param1 + param2
            i += 4
        elif opcode == 2:
            param1 = ic[ic[i + 1]] if mode1 == 0 else ic[i + 1]
            param2 = ic[ic[i + 2]] if mode2 == 0 else ic[i + 2]
            result_pos = ic[i + 3]
            ic[result_pos] = param1 * param2
            i += 4
        elif opcode == 3:
            param1 = ic[i + 1]
            ic[param1] = input_integer
            i += 2
        elif opcode == 4:
            param1 = ic[ic[i + 1]] if mode1 == 0 else ic[i + 1]
            outputs.append(param1)
            i += 2
        elif opcode == 5:
            param1 = ic[ic[i + 1]] if mode1 == 0 else ic[i + 1]
            param2 = ic[ic[i + 2]] if mode2 == 0 else ic[i + 2]
            if param1 != 0:
                i = param2
            else:
                i += 3
        elif opcode == 6:
            param1 = ic[ic[i + 1]] if mode1 == 0 else ic[i + 1]
            param2 = ic[ic[i + 2]] if mode2 == 0 else ic[i + 2]
            if param1 == 0:
                i = param2
            else:
                i += 3
        elif opcode == 7:
            param1 = ic[ic[i + 1]] if mode1 == 0 else ic[i + 1]
            param2 = ic[ic[i + 2]] if mode2 == 0 else ic[i + 2]
            result_pos = ic[i + 3]
            if param1 < param2:
                ic[result_pos] = 1
            else:
                ic[result_pos] = 0
            i += 4
        elif opcode == 8:
            param1 = ic[ic[i + 1]] if mode1 == 0 else ic[i + 1]
            param2 = ic[ic[i + 2]] if mode2 == 0 else ic[i + 2]
            result_pos = ic[i + 3]
            if param1 == param2:
                ic[result_pos] = 1
            else:
                ic[result_pos] = 0
            i += 4

    return {'intcode': ic, 'outputs': outputs}

def find_noun_and_verb(output, intcode, min_noun, max_noun, min_verb, max_verb):
    # Note: the noun and verb are both between 0 and 99
    for noun in range(min_noun, max_noun):
        for verb in range(min_verb, max_verb):
            if process_intcode([intcode[0], noun, verb] + intcode[3:], 1)['intcode'][0] == output:
                return 100 * noun + verb
    return 'No possible noun/verb combination was found'

############### DAY 3 ###############
def find_closest_intersection(paths):
    intersections = find_all_intersections(paths)
    intersection_points = []

    for i in intersections:
        if i[0]['direction'] == 'HORIZONTAL' and i[1]['direction'] == 'VERTICAL':
            intersection_points.append(get_perp_intersection_point(i[0], i[1]))
        elif i[0]['direction'] == 'VERTICAL' and i[1]['direction'] == 'HORIZONTAL':
            intersection_points.append(get_perp_intersection_point(i[1], i[0]))
        # Handle colinear stuff later

    manhattan_distances = []
    for p in intersection_points:
        manhattan_distances.append(determine_manhattan_distance(p))

    return min(manhattan_distances)

def find_earliest_signal_overlap(paths):
    intersections = find_all_intersections(paths)
    total_signal_distances = []

    for i in intersections:
        if i[0]['direction'] == 'HORIZONTAL' and i[1]['direction'] == 'VERTICAL':
            first_signal_distance = i[0]['total_distance_before'] + abs(i[0]['start'][0] - i[1]['start'][0])
            second_signal_distance = i[1]['total_distance_before'] + abs(i[1]['start'][1] - i[0]['start'][1])
            total_signal_distances.append(first_signal_distance + second_signal_distance)
        elif i[0]['direction'] == 'VERTICAL' and i[1]['direction'] == 'HORIZONTAL':
            first_signal_distance = i[0]['total_distance_before'] + abs(i[0]['start'][1] - i[1]['start'][1])
            second_signal_distance = i[1]['total_distance_before'] + abs(i[1]['start'][0] - i[0]['start'][0])
            total_signal_distances.append(first_signal_distance + second_signal_distance)
    
    return min(total_signal_distances)

def find_all_intersections(paths):
    first_segments = setup_point_arr(paths['first'])
    second_segments = setup_point_arr(paths['second'])
    all_intersections = []

    for i in range(0, len(first_segments)):
        for j in range(0, len(second_segments)):
            has_intersection = check_for_instersection(first_segments[i], second_segments[j])

            if has_intersection:
                all_intersections.append([first_segments[i], second_segments[j]])
    
    return all_intersections
    
def setup_point_arr(path):
    segments = []
    end_point = [0,0]
    total_distance_traveled = 0
    for move in path:
        # Start point of each segment is the end point of the previous segment
        end_point_stats = get_end_point(end_point, move)
        new_end_point = end_point_stats['point']
        distance = end_point_stats['distance']

        segments.append({
            'start': end_point,
            'end': new_end_point,
            'total_distance_before': total_distance_traveled,
            'direction': determine_direction(end_point, new_end_point)
        })
        end_point = new_end_point
        total_distance_traveled = total_distance_traveled + distance
    
    return segments

def get_end_point(start_point, move):
    # points have the format: [x, y]
    direction = move[0].upper()
    distance = int(move[1:])
    point = [0,0]
    if direction == 'R':
        point = [start_point[0] + distance, start_point[1]]
    elif direction == 'L':
        point =  [start_point[0] - distance, start_point[1]]
    elif direction == 'U':
        point =  [start_point[0], start_point[1] + distance]
    elif direction == 'D':
        point =  [start_point[0], start_point[1] - distance]
    
    return {'point': point, 'distance': distance}

def check_for_instersection(first, second):
    # Checks if lines follow the same path (checks if they are on the same line
    # and if so, checks if the start of either segment is within the other)
    if first['direction'] == 'HORIZONTAL' and second['direction'] == 'HORIZONTAL' and first['start'][1] == second['start'][1]:
        return is_colinear([first['start'][0], first['end'][0]], [second['start'][0], second['end'][0]])

    if first['direction'] == 'VERTICAL' and second['direction'] == 'VERTICAL' and first['start'][0] == second['start'][0]:
        return is_colinear([first['start'][0], first['end'][0]], [second['start'][0], second['end'][0]])
    
    # # At this point, I know the lines are perpindicular, check for crossing
    if first['direction'] == 'HORIZONTAL':
        # Second has to be vertical then
        return check_for_perpindicular_cross(first, second)
    else:
        # Second has to be the horizontal
        return check_for_perpindicular_cross(second, first)

# For each segment, make sure the start and end are in order (going up and to the right are considered positive dierections)
def format_segment(segment):
    if segment['direction'] == 'HORIZONTAL':
        start = segment['start']
        end = segment['end']
        if start[0] > end[0]:
            return {
                'start': end,
                'end': start,
                'direction': segment['direction'] 
            }
        return segment
    else: # is a vertical line
        start = segment['start']
        end = segment['end']
        if start[1] > end[1]:
            return {
                'start': end,
                'end': start,
                'direction': segment['direction'] 
            }
        return segment

def check_for_perpindicular_cross(horizontal_segment, vertical_segment):
    # Check if the y-position of the horizontal is within the y of the vertical
    ho_start = horizontal_segment['start']
    ho_end = horizontal_segment['end']
    vert_start = vertical_segment['start']
    vert_end = vertical_segment['end']

    return is_between(ho_start[1], [vert_start[1], vert_end[1]]) and is_between(vert_start[0], [ho_start[0], ho_end[0]])

def determine_direction(start, end):
    if start[0] == end[0]:
        return 'VERTICAL'
    return 'HORIZONTAL'

# first and second are only in one dimension - type: [start, end]
# where the start and end are just the points in the desired dimension
def is_colinear(first, second):
    return is_between(first[0], second) or is_between(first[1], second)

def is_between(number, between_arr):
    return min(between_arr) <= number <= max(between_arr)

def get_perp_intersection_point(horizontal_segment, vertical_segment):
    return [horizontal_segment['start'][1], vertical_segment['start'][0]]

def determine_manhattan_distance(point):
    return abs(point[0]) + abs(point[1])

############### DAY 4 ###############
# It is a six-digit number.
# The value is within the range given in your puzzle input.
# Two adjacent digits are the same (like 22 in 122345).
# Going from left to right, the digits never decrease; they only ever increase or stay the same (like 111123 or 135679).
def find_possible_fuel_passwords(password_range, difficulty):
    range_min = min(password_range)
    range_max = max(password_range)
    possible_passwords = []

    for i in range(range_min, range_max, 1):
        # in case the number is 5-digit or less
        password = str(i).zfill(6)
        if difficulty == 'SIMPLE':
            if has_at_least_double_number(password) and never_decreases(password):
                possible_passwords.append(password)
        elif difficulty == 'COMPLEX':
            if has_double_number(password) and never_decreases(password):
                possible_passwords.append(password)

    return possible_passwords

def has_at_least_double_number(password):
    for l in range(1, len(password)):
        if password[l] == password[l - 1]:
            return True
    return False

def has_double_number(password):
    current_count = 0
    current_char = ''
    summary = []
    for l in range(0, len(password)):
        if password[l] == current_char:
            current_count = current_count + 1
        else:
            summary.append(current_count)
            current_char = password[l]
            current_count = 1

    summary.append(current_count)
    
    return 2 in summary

def never_decreases(password):
    for l in range(1, len(password)):
        if int(password[l]) < int(password[l - 1]):
            return False
    return True

############### DAY 5 ###############
# Calculated using the modified Intcode computer from day 2

############### DAY 6 ###############
def calculate_total_orbits(orbits):
    split_orbits = get_split_orbits(orbits)
    planets = get_all_planets(split_orbits)
    
    total_orbits = 0
    for planet in planets:
        # Subtract one because it is the number of paths to the center
        # (one less than the number of planets)
        total_orbits += len(get_path_to_com(split_orbits, planet)) - 1
    
    return total_orbits

def get_split_orbits(orbits):
    split_orbits = []
    for orbit in orbits:
        split_orbits.append(orbit.split(')'))
    
    return split_orbits

def get_all_planets(split_orbits):
    planets = {}
    for orbit in split_orbits:
        planets[orbit[0]] = 0
        planets[orbit[1]] = 0
    
    result = []
    for p in planets:
        result.append(p)

    return result
    
# Returns an array pathing to the center of mass: ['C', 'B', 'A', 'COM']
def get_path_to_com(split_orbits, planet):
    current_planet = planet
    orbit_count = [current_planet]
    while current_planet != 'COM':
        for o in split_orbits:
            if o[1] == current_planet:
                current_planet = o[0]
                orbit_count.append(current_planet)
    return orbit_count

def calculate_orbital_transfers(orbits, start, end):
    split_orbits = get_split_orbits(orbits)

    path1 = get_path_to_com(split_orbits, start)
    path2 = get_path_to_com(split_orbits, end)

    path2_set = set()
    for p in path2:
        path2_set.add(p)
    
    intersections = []
    for i in range(0, len(path1)):
        current = path1[i]
        if current in path2_set:
            # subract 2 because the first transfer happens from index 1 to 2 in each path
            intersections.append(i + path2.index(current) - 2)

    return min(intersections)            


############### RESULTS ###############
def print_results():
    print(f'Day 1.1: {simple_fuel_requirements(day_1_input)}')
    print(f'Day 1.2: {complex_fuel_requirements(day_1_input)}')
    print(f'Day 2.1: {process_intcode([day_2_input[0], 12, 2] + day_2_input[3:], 1)["intcode"][0]}')
    print(f'Day 2.2: {find_noun_and_verb(19690720, day_2_input, 0, 99, 0, 99)}')
    print(f'Day 3.1: {find_closest_intersection(day_3_input)}')
    print(f'Day 3.2: {find_earliest_signal_overlap(day_3_input)}')
    print(f'Day 4.1: {len(find_possible_fuel_passwords(day_4_input, "SIMPLE"))}')
    print(f'Day 4.2: {len(find_possible_fuel_passwords(day_4_input, "COMPLEX"))}')
    print(f'Day 5.1: {process_intcode(day_5_input, 1)["outputs"][-1]}')
    print(f'Day 5.2: {process_intcode(day_5_input, 5)["outputs"][-1]}')
    print(f'Day 6.1: {calculate_total_orbits(day_6_input)}')
    print(f'Day 6.2: {calculate_orbital_transfers(day_6_input, "YOU", "SAN")}')

print_results()
