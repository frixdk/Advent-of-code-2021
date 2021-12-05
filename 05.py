from collections import Counter

import click
from aocd import lines
from aocd import submit as aocd_submit

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version="0.0.1")
def advent():
    pass


def parse_input(input):
    all_lines = []
    horizontal_vertical_lines = []

    for entry in input:
        start, _, end = entry.split()

        x1 = int(start.split(",")[0])
        y1 = int(start.split(",")[1])
        x2 = int(end.split(",")[0])
        y2 = int(end.split(",")[1])

        points = []

        if x1 == x2:
            for y in range(y1, y2, 1 if y1 < y2 else -1):
                points.append((x1, y))
        elif y1 == y2:
            for x in range(x1, x2, 1 if x1 < x2 else -1):
                points.append((x, y1))
        else:
            xs = list(range(x1, x2, 1 if x1 < x2 else -1))
            ys = list(range(y1, y2, 1 if y1 < y2 else -1))

            for p in list(zip(xs, ys)):
                points.append(p)

        points.append((x2, y2))

        all_lines.append(points)
        if x1 == x2 or y1 == y2:
            horizontal_vertical_lines.append(points)

    return all_lines, horizontal_vertical_lines


def a_solver(input):
    _, lines = parse_input(input)
    points = [p for line in lines for p in line]
    intersections = [item for item, count in Counter(points).items() if count > 1]

    return len(intersections)


def b_solver(input):
    lines, _ = parse_input(input)
    points = [p for line in lines for p in line]
    intersections = [item for item, count in Counter(points).items() if count > 1]

    return len(intersections)


@advent.command()
def test():
    test_input = [
        "0,9 -> 5,9",
        "8,0 -> 0,8",
        "9,4 -> 3,4",
        "2,2 -> 2,1",
        "7,0 -> 7,4",
        "6,4 -> 2,0",
        "0,9 -> 2,9",
        "3,4 -> 1,4",
        "0,0 -> 8,8",
        "5,5 -> 8,2"
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
