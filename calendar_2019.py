import math
from data_2019 import day_1_input, day_2_input

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
def process_intcode(intcode):
    for i in range(0, len(intcode), 4):
        operator = intcode[i]
        if operator == 99:
            return intcode[0]

        first_pos = intcode[i + 1]
        second_pos = intcode[i + 2]
        result_pos = intcode[i + 3]
        result = 0
        if operator == 1:
            result = intcode[first_pos] + intcode[second_pos]
        elif operator == 2:
            result = intcode[first_pos] * intcode[second_pos]
        else:
            return f'Something went wrong at index {i}'
        intcode[result_pos] = result
    return 'Never found the end code'

############### RESULTS ###############
def print_results():
    print(f'Day 1.1: {simple_fuel_requirements(day_1_input)}')
    print(f'Day 1.2: {complex_fuel_requirements(day_1_input)}')
    print(f'Day 2.1: {process_intcode([day_2_input[0], 12, 2] + day_2_input[3:])}')

print_results()