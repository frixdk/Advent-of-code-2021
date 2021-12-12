from collections import Counter, defaultdict

import click
from aocd import lines
from aocd import submit as aocd_submit

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version="0.0.1")
def advent():
    pass


def parse_input(edges):
    nodes = defaultdict(set)

    for edge in edges:
        n, m = edge.split("-")
        nodes[n].add(m)
        nodes[m].add(n)

    return nodes


def a_solver(input):
    nodes = parse_input(input)

    possible_paths = [["start"]]

    paths = []

    while(possible_paths):
        extended_paths = []
        for path in possible_paths:
            if path[-1] == "end":
                paths.append(path)
            for node in nodes[path[-1]]:
                if node.islower() and node in path:
                    pass
                else:
                    extended_paths.append(path + [node])

        possible_paths = extended_paths

    return len(paths)


def path_has_double_visit(path):
    small_caves = [n for n in path if n.islower()]
    c = Counter(small_caves)

    doubles = [k for k, v in c.items() if v > 1]
    if doubles:
        return True
    else:
        return False


def b_solver(input):
    nodes = parse_input(input)

    possible_paths = [["start"]]

    paths = []

    while(possible_paths):
        extended_paths = []
        for path in possible_paths:
            if path[-1] == "end":
                paths.append(path)
            for node in nodes[path[-1]]:
                if node in ["start", "end"] and node in path:
                    pass
                elif node.islower() and node in path:
                    # exception
                    if not path_has_double_visit(path):
                        extended_paths.append(path + [node])
                else:
                    extended_paths.append(path + [node])

        possible_paths = extended_paths

    return len(paths)


@advent.command()
def test():
    test_input = [
        "start-A",
        "start-b",
        "A-c",
        "A-b",
        "b-d",
        "A-end",
        "b-end"
    ]

    print("A result:", a_solver(test_input))
    print("B result:", b_solver(test_input))


@advent.command()
def solve():
    print("A result:", a_solver(lines))
    print("B result:", b_solver(lines))


@advent.command()
def submit():
    aocd_submit(a_solver(lines), part="a")
    aocd_submit(b_solver(lines), part="b")


if __name__ == "__main__":
    advent()
