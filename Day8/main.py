# FILENAME = "sample_input.txt"
FILENAME = "input.txt"

import time
import utils
from collections import Counter


def main():
    start_time = time.time()

    data = parse_data()
    parse_time = time.time()

    answer1 = part1(data)
    part1_time = time.time()
    answer2 = part2(data)
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
        data = f.read()

    return data.strip()


def part1(data):

    layers = []
    for x in range(0, len(data), 150):
        layers.append(data[x:x+150])

    num_zeros = 151
    zero_layer = 151
    counts = {}
    for i,layer in enumerate(layers):
        count = Counter(layer)
        counts[i] = count
        if count[str(0)] < num_zeros:
            num_zeros = count[str(0)]
            zero_layer = i
    
    return counts[zero_layer][str(1)] * counts[zero_layer][str(2)]
    

def part2(data):

    image = [2]*150
    for x in range(150):
        image[x] = data[x]
    for x in range(150, len(data), 150):
        for i in range(x, x+150):
            if image[i%150] == "2":
                image[i%150] = data[i]
        count = Counter(image)
        if count[str(2)] == 0:
            break

    for i in range(0, 6):
        for j in range(25):
            # print(i,j)
            if image[i*25+j] == str(1):
                print("#", end="")
            else:
                print(" ", end="")
        print()


    return None


if __name__ == "__main__":
    main()