import math

import click
from aocd import lines
from aocd import submit as aocd_submit

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version="0.0.1")
def advent():
    pass


def parse_input(map_lines):
    map = {}
    for y, map_line in enumerate(map_lines):
        for x, n in enumerate(map_line):
            map[(x, y)] = int(n)

    return map, len(map_lines[0]), len(map_lines)


def a_solver(input):
    map, width, height = parse_input(input)

    low = 0

    for x in range(width):
        for y in range(height):
            n = map[(x, y)]

            if (
                    n < map.get((x, y-1), 10) and
                    n < map.get((x, y+1), 10) and
                    n < map.get((x-1, y), 10) and
                    n < map.get((x+1, y), 10)
            ):
                low += n + 1

    return low


def build_basin(map, basin):
    new_coords = set()
    for x, y in basin:
        n = map[(x, y)]

        consider = [
            (x, y-1),
            (x, y+1),
            (x-1, y),
            (x+1, y),
        ]

        for con in consider:
            con_n = map.get(con)
            if con_n and con_n > n and con_n < 9 and con not in basin:
                new_coords.add(con)

    if len(new_coords) > 0:
        basin.update(new_coords)
        return build_basin(map, basin)
    else:
        return basin


def b_solver(input):
    map, width, height = parse_input(input)

    lows = []

    for x in range(width):
        for y in range(height):
            n = map[(x, y)]

            if (
                    n < map.get((x, y-1), 10) and
                    n < map.get((x, y+1), 10) and
                    n < map.get((x-1, y), 10) and
                    n < map.get((x+1, y), 10)
            ):
                lows.append(set([(x, y)]))

    basins = []
    for low in lows:
        basins.append(build_basin(map, low))

    return math.prod(sorted([len(basin) for basin in basins])[-3:])


@advent.command()
def test():
    test_input = [
        "2199943210",
        "3987894921",
        "9856789892",
        "8767896789",
        "9899965678"
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
