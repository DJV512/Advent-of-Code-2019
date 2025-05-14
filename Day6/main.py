# FILENAME = "sample_input.txt"
FILENAME = "input.txt"

import time
import utils
import networkx as nx
from functools import lru_cache
from collections import deque


def main():
    start_time = time.time()

    data = parse_data()
    parse_time = time.time()

    answer1, G = part1(data)
    part1_time = time.time()
    answer2 = part2(G)
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

    planets = []
    for line in data:
        orbited, orbiter = line.strip().split(")")
        planets.append((orbited, orbiter))
    return planets


@lru_cache(maxsize=None)
def count_nodes(G, node, steps):
    if node == "COM":
        return steps
    else:
        for key in G.adj[node]:
            steps = count_nodes(G, key, steps + 1)
    
    return steps


def part1(data):

    G = nx.DiGraph()

    for orbited, orbiter in data:
        G.add_edge(orbiter, orbited)

    total = 0
    for node in G.nodes:
        total += count_nodes(G, node, 0)

    return total, G


def part2(G):

    new_G = nx.Graph(G)
    sp = dict(nx.all_pairs_shortest_path(new_G))
    return(len(sp["YOU"]["SAN"])-3)


if __name__ == "__main__":
    main()