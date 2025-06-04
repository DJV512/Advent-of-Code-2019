# FILENAME = "sample_input.txt"
FILENAME = "input.txt"

import time
import utils
import heapq
from collections import defaultdict, deque
from copy import copy


def main():
    start_time = time.time()

    data1, data2 = parse_data()
    parse_time = time.time()

    answer1, keys = part1(data1)
    part1_time = time.time()
    answer2 = part2(data2, keys)
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
        data1 = f.readlines()
    
    with open("input2.txt", "r") as f:
        data2 = f.readlines()

    return utils.grid_parse_dict(data1), utils.grid_parse_dict(data2)


def part1(data):

    max_y = max(y for y,x in data.keys())
    max_x = max(x for y,x in data.keys())
    
    keys = dict()
    for y in range(max_y+1):
        for x in range(max_x+1):
            if 97 <= ord(data[(y,x)]) <= 122:
                keys[data[y,x]] = (y, x)
            elif ord(data[(y,x)]) == 64:
                start = (y,x)
    
    num_keys = len(keys)

    visited = defaultdict(set)

    target_mask = (1 << num_keys) - 1

    pq = []
    heapq.heappush(pq, (0, start, 0))

    while pq:
        steps, position, key_mask = heapq.heappop(pq)
        
        if 65 <= ord(data[position]) <= 90:
            bit_index = (ord(data[position].lower())-ord('a'))
            if ((key_mask >> bit_index) & 1) == 0:
                continue
        
        if 97 <= ord(data[position]) <= 122:
            bit_index = ord(data[position]) - ord('a')
            if ((key_mask >> bit_index) & 1) == 0:
                key_mask |= 1 << bit_index

        if key_mask == target_mask:
            return steps, keys

        if any(prev_mask | key_mask == prev_mask for prev_mask in visited[position]):
            continue
        else:
            visited[position] = {x for x in visited[position] if x | key_mask != key_mask}
            visited[position].add(key_mask)

        for direction in utils.DIRS_4:
            next_position = (position[0] + direction[0], position[1] + direction[1])

            if 0 <= next_position[0] <= max_y and 0 <= next_position[1] <= max_x and data[next_position] != "#":
                if any(prev_mask | key_mask == prev_mask for prev_mask in visited[next_position]):
                    continue
                else:   
                    heapq.heappush(pq, (steps + 1, next_position, key_mask))


def key_to_key(data, start_key, keys, max_x, max_y):

    distances = defaultdict(list)
    start = keys[start_key]
    queue = deque()
    visited = set()
    queue.append((start, 0, tuple()))

    while queue:

        position, steps, doors = queue.popleft()

        if 65 <= ord(data[position]) <= 90:
            doors = doors + (data[position],)

        if 97 <= ord(data[position]) <= 122 and data[position] != start_key:
            distances[start_key].append((data[position], steps, doors))

        visited.add(position)

        for direction in utils.DIRS_4:
            next_position = (position[0] + direction[0], position[1] + direction[1])

            if 0 <= next_position[0] <= max_y and 0 <= next_position[1] <= max_x and data[next_position] != "#" and next_position not in visited:
                queue.append((next_position, steps+1, doors))

    return distances



def part2(data, keys):

    max_y = max(y for y,x in data.keys())
    max_x = max(x for y,x in data.keys())

    robots = {}
    robot_num = 1
    for y in range(max_y+1):
        for x in range(max_x+1):
            if data[(y,x)] == "@":
                robots[f"@{robot_num}"] = (y,x)
                robot_num += 1

    nodes = keys.copy() | robots

    distances = []
    for key in nodes:
        distances.append(key_to_key(data, key, nodes, max_x, max_y))

    key_map = {}
    for distance in distances:
        key_map = key_map | distance

    final_key_map = defaultdict(list)
    for key in key_map:
        for dest_key, steps, keys_needed in key_map[key]:
            keys_needed_bitmask = 0
            for key_needed in keys_needed:
                bit_index = ord(key_needed.lower()) - ord('a')
                keys_needed_bitmask |= 1 << bit_index
            final_key_map[key].append((dest_key, steps, keys_needed_bitmask))

    num_keys = len(keys)
    visited = defaultdict(set)
    target_mask = (1 << num_keys) - 1

    pq = []
    heapq.heappush(pq, (0, "@1", "@2", "@3", "@4", 0))

    while pq:
        steps, r1, r2, r3, r4, key_mask = heapq.heappop(pq)

        if key_mask == target_mask:
            return steps
        
        if any(prev_mask | key_mask == prev_mask for prev_mask in visited[(r1, r2, r3, r4)]):
            continue
        else:
            visited[(r1, r2, r3, r4)] = {x for x in visited[(r1, r2, r3, r4)] if x | key_mask != key_mask}
            visited[(r1, r2, r3, r4)].add(key_mask)

        for dest_key, next_steps, keys_needed_bitmask in final_key_map[r1]:
            if keys_needed_bitmask | key_mask == key_mask:
                new_key_mask = key_mask | 1 << (ord(dest_key)-ord("a"))
                if any(prev_mask | new_key_mask == prev_mask for prev_mask in visited[(dest_key, r2, r3, r4)]):
                    continue
                else:    
                    heapq.heappush(pq, (steps+next_steps, dest_key, r2, r3, r4, new_key_mask))
        
        for dest_key, next_steps, keys_needed_bitmask in final_key_map[r2]:
            if keys_needed_bitmask | key_mask == key_mask:
                new_key_mask = key_mask | 1 << (ord(dest_key)-ord("a"))
                if any(prev_mask | new_key_mask == prev_mask for prev_mask in visited[(r1, dest_key, r3, r4)]):
                    continue
                else:   
                    heapq.heappush(pq, (steps+next_steps, r1, dest_key, r3, r4, new_key_mask))
        
        for dest_key, next_steps, keys_needed_bitmask in final_key_map[r3]:
            if keys_needed_bitmask | key_mask == key_mask:
                new_key_mask = key_mask | 1 << (ord(dest_key)-ord("a"))
                if any(prev_mask | new_key_mask == prev_mask for prev_mask in visited[(r1, r2, dest_key, r4)]):
                    continue
                else:  
                    heapq.heappush(pq, (steps+next_steps, r1, r2, dest_key, r4, new_key_mask))
        
        for dest_key, next_steps, keys_needed_bitmask in final_key_map[r4]:
            if keys_needed_bitmask | key_mask == key_mask:
                new_key_mask = key_mask | 1 << (ord(dest_key)-ord("a"))
                if any(prev_mask | new_key_mask == prev_mask for prev_mask in visited[(r1, r2, r3, dest_key)]):
                    continue
                else:  
                    heapq.heappush(pq, (steps+next_steps, r1, r2, r3, dest_key, new_key_mask))


       


if __name__ == "__main__":
    main()