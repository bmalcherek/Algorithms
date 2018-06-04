# Data in text file "plecak.txt", first line is number of elements and size of backpack
# Second line is sizes of elements
# Third line is values of elements
# All values in the file are separated by space

# This code solve the knapsack problem in 3 ways - brute force, greedy algorithm (ratio) and dynamic algorithm. It was
# used in my algorithm course in Poznan University of Technology to measure time and result difference between these
# algorithms.

import time

# Importing the data from text file

data = open("plecak.txt")
elements = list()
sizeOfBackpack = 0
numberOfElements = 0

it = 0
for line in data:
    line = line.replace("\n", "")
    line = line.split(" ")
    if it == 0:
        numberOfElements = int(line[0])
        sizeOfBackpack = int(line[1])
    elif it == 1:
        for j in range(len(line)):
            elements.append([int(line[j])])
    elif it == 2:
        for j in range(len(line)):
            elements[j].append(int(line[j]))
    it += 1
del it


# BRUTE FORCE


def brute_force(a_list):
    start_time = time.time()
    # Generating binary number to iterate through all possibilities
    possibilities = 2 ** numberOfElements - 1
    binary_choice = bin(possibilities)
    best = ""
    best_value = 0
    # Loop until all possibilities are checked
    while int(binary_choice, 2) > 0:
        temp_size = 0
        temp_value = 0
        backpack = list()
        # Stripping "0b" from binary number, because converted int number to binary is converted to string as "0b + binary"
        binary = binary_choice[2:]
        iterator = 0
        # Checking order:
        # 11111, 11110, ..., 10000
        # 01111, 01110, ..., 01000
        # So I need to maintain the same length of string to check all combinations, therefore I need to add "0" at beginning of the string
        if len(binary) < numberOfElements:
            to_add = numberOfElements - len(binary)
            to_add_str = "0" * to_add
            binary = to_add_str + binary
        # Collecting elements to current combination of knapsack from the list of all elements
        for char in binary:
            if char == "1":
                backpack.append(a_list[iterator])
            iterator = iterator + 1
        # Scoring current iteration of backpack
        for element in backpack:
            temp_size += int(element[0])
            temp_value += int(element[1])
        # Evaluating if current knapsack is better than current best
        if temp_size <= sizeOfBackpack and temp_value > best_value:
            best_value = temp_value
            best = binary
        # Switching to the next iteration
        binary_choice = int(binary_choice, 2)
        binary_choice -= 1
        binary_choice = bin(binary_choice)
    return best, best_value, time.time() - start_time


# VALUE/WEIGHT ALGORITHM


def ratio(a_list):
    start_time = time.time()
    calculated_ratios = list()
    # Calculating value to weight ratio of every element
    for i in range(len(a_list)):
        rat = a_list[i][1] / a_list[i][0]
        calculated_ratios.append([rat, i, a_list[i][0], a_list[i][1]])
    # Sorting list of all elements by ratio in decreasing order
    calculated_ratios = sorted(calculated_ratios, reverse=True)
    used_capacity = 0
    result = list()
    value = 0
    # Loop through every element
    for element in calculated_ratios:
        # If element fit into knapsack, then put in into knapsack, and increase value of backpack 
        if element[2] + used_capacity <= sizeOfBackpack:
            used_capacity += element[2]
            result.append(element[1])
            value += element[3]
    return result, value, time.time() - start_time


# DYNAMIC ALGORITHM

def dynamic(a_list):
    start_time = time.time()
    # Creating 2 2D arrays, one to keep the values, and one to keep track of if element is in backpack
    b = [[0] * (sizeOfBackpack + 1) for i in range(numberOfElements)]
    keep = [[0] * (sizeOfBackpack + 1) for i in range(numberOfElements)]
    i = 0
    for element in a_list:
        for k in range(sizeOfBackpack + 1):
            # If element fits to knapsack, evaluate value of knapsack with and without that element and either take it or not
            if k >= element[0]:
                value_with = b[i - 1][k - element[0]] + element[1]
                value_without = b[i - 1][k]
                if value_without > value_with:
                    keep[i][k] = 0
                    b[i][k] = value_without
                else:
                    keep[i][k] = 1
                    b[i][k] = value_with
            # If element doesn't fit, take the value of knapsack which is one row higher in table
            else:
                b[i][k] = b[i - 1][k]
                keep[i][k] = 0
        i = i + 1
    remaining_capacity = sizeOfBackpack
    result = list()
    value = 0
    # Iterate through array, take elements from best score and evaluate the score
    for i in range(numberOfElements - 1, -1, -1):
        if keep[i][remaining_capacity] == 1:
            result.append(i)
            value += a_list[i][1]
            remaining_capacity -= a_list[i][0]
    return result, value, time.time() - start_time


print(brute_force(list(elements)))
print(dynamic(list(elements)))
print(ratio(list(elements)))
