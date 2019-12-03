import math
from data_2019 import fuel_modules

def calculate_simple_fuel(module):
    return math.floor(module / 3) - 2

def calculate_complex_fuel(module):
    total_fuel = 0
    fuel_req = calculate_simple_fuel(module)
    if fuel_req > 0:
        total_fuel += fuel_req + total_fuel + calculate_complex_fuel(fuel_req)
    return total_fuel

# Day 1 - Part 1
def simple_fuel_requirements():
    total_fuel = 0
    for module in fuel_modules:
        total_fuel += calculate_simple_fuel(module)
    return total_fuel

# Day 1 - Part 2
def complex_fuel_requirements():
    total_fuel = 0
    for module in fuel_modules:
        total_fuel += calculate_complex_fuel(module)
    return total_fuel

def print_results():
    print(f'Day 1.1: {simple_fuel_requirements()}')
    print(f'Day 1.2: {complex_fuel_requirements()}')

print_results()