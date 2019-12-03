from data_2019 import *
import math

def calculate_single_basic_fuel_requirements(module):
    return math.floor(module / 3) - 2

# Day 1 - Part 1
def simple_fuel_requirements():
    total_fuel = 0
    for module in fuel_modules:
        total_fuel += calculate_single_basic_fuel_requirements(module)
    return total_fuel

print(f'Day 1 - Part 1: {simple_fuel_requirements()}')
