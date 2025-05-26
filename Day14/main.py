# FILENAME = "sample_input.txt"
FILENAME = "input.txt"

import time
import utils
from collections import defaultdict


def main():
    start_time = time.time()

    data = parse_data()
    parse_time = time.time()

    answer1 = part1(data)
    part1_time = time.time()
    answer2 = part2(data, answer1)
    part2_time = time.time()

    print("---------------------------------------------------")
    print(f"Part 1 Answer: {answer1}")
    print()
    print(f"Part 2 Answer: {answer2}")
    print()
    print(f"Data Parse Execution Time: {1000*(parse_time - start_time):.2f} ms")
    print(f"Part 1 Execution Time:     {1000*(part1_time - parse_time):.2f} ms")
    print(f"Part 2 Execution Time:     {1000*(part2_time - part1_time):.2f} ms")
    print(f"Total Execution Time:      {1000*(part2_time - start_time):.2f} ms")
    print("---------------------------------------------------")


output = True  # Toggle this flag to enable/disable prints
def debug_print(*args, **kwargs):
    if output:
        print(*args, **kwargs)


def parse_data():
    with open(FILENAME, "r") as f:
        data = f.readlines()

    reactions = {}
    for line in data:
        parts = line.strip().split("=>")
        quantity, chemical = parts[1].split()
        if "ORE" in parts[0]:
            ore_quant, ore_chem = parts[0].split()
            reactions[chemical] = [int(quantity), (ore_chem, int(ore_quant))]
        else:
            subparts = parts[0].split(", ")
            reactions[chemical] = [int(quantity)]
            for subpart in subparts:
                q, chem = subpart.split()
                reactions[chemical].append((chem, int(q)))

    return reactions


def part1(data):

    queue = defaultdict(int)
    queue["FUEL"] = 1

    inventory = {}
    used = {}
    used["ORE"] = 0
    inventory["ORE"] = 0

    while queue:


        chemical, quantity_needed = queue.popitem()

        if chemical == "ORE":
            used["ORE"] += quantity_needed
            continue

        for i, input in enumerate(data[chemical]):

            if i == 0:
                quantity_produced_in_one_reaction = input
            else:
                ingredient, amount = input
                if quantity_needed % quantity_produced_in_one_reaction == 0:
                    needed = quantity_needed / quantity_produced_in_one_reaction
                else:
                    needed = quantity_needed // quantity_produced_in_one_reaction + 1

                total_needed = needed*amount

                if ingredient in inventory and inventory[ingredient] > total_needed:
                    inventory[ingredient] -= total_needed
                elif ingredient in inventory:
                    queue[ingredient] += int(total_needed)-inventory[ingredient]
                    inventory[ingredient] = 0
                else:
                    queue[ingredient] += int(total_needed)
                inventory[chemical] = int(needed*quantity_produced_in_one_reaction) - quantity_needed
                used[chemical] = quantity_needed

    return used["ORE"] + inventory["ORE"]


def part2(data, answer1):

    starting_guess = 1000000000000//answer1
    backward = False

    while True:

        queue = defaultdict(int)
        queue["FUEL"] = starting_guess

        inventory = {}
        used = {}
        used["ORE"] = 0
        inventory["ORE"] = 0

        while queue:


            chemical, quantity_needed = queue.popitem()

            if chemical == "ORE":
                used["ORE"] += quantity_needed
                continue

            for i, input in enumerate(data[chemical]):

                if i == 0:
                    quantity_produced_in_one_reaction = input
                else:
                    ingredient, amount = input
                    if quantity_needed % quantity_produced_in_one_reaction == 0:
                        needed = quantity_needed / quantity_produced_in_one_reaction
                    else:
                        needed = quantity_needed // quantity_produced_in_one_reaction + 1

                    total_needed = needed*amount

                    if ingredient in inventory and inventory[ingredient] > total_needed:
                        inventory[ingredient] -= total_needed
                    elif ingredient in inventory:
                        queue[ingredient] += int(total_needed)-inventory[ingredient]
                        inventory[ingredient] = 0
                    else:
                        queue[ingredient] += int(total_needed)
                    inventory[chemical] = int(needed*quantity_produced_in_one_reaction) - quantity_needed
                    used[chemical] = quantity_needed
        
        ore_used = used["ORE"] + inventory["ORE"]
        if ore_used > 1000000000000:
            backward = True
            starting_guess -= 1
        else:
            if backward:
                return starting_guess
            else:
                starting_guess += 100

    



if __name__ == "__main__":
    main()