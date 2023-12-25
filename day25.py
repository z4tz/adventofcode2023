from inputreader import aocinput
import os
import networkx as nx


def find_groups(data: list[str]):
    graph = nx.Graph()
    for line in data:

        base, rest = line.strip().split(':')
        parts = rest.split()
        for part in parts:
            graph.add_edge(base, part)
    groups = nx.community.louvain_communities(graph, resolution=0.1)
    return len(groups[0]) * len(groups[1])


def main(day: int):
    data = aocinput(day)
    results = find_groups(data)
    print(results)


if __name__ == '__main__':
    main(int(os.path.basename(__file__)[3:-3]))
