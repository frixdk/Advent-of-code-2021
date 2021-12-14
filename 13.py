from collections import Counter, defaultdict

import click
from aocd import lines
from aocd import submit as aocd_submit

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version="0.0.1")
def advent():
    pass


def parse_input(input):
    dots = []
    instructions = []
    for i in input:
        dot = i.split(",")

        if len(dot) == 2:
            dots.append(tuple([int(d) for d in dot]))

        if "fold along" in i:
            ins = i.split("=")
            instructions.append((ins[0][-1], int(ins[1])))

    return dots, instructions


def a_solver(input):
    dots, instructions = parse_input(input)

    print(dots)
    print(instructions)

    for index, dot in enumerate(dots):
        x, y = dot
        direction, value = instructions[0]
        if direction == "y":
            if y > value:
                dots[index] = (x, value-(y-value))
        if direction == "x":
            if x > value:
                dots[index] = (value-(x-value), y)

    return len(set(dots))


def b_solver(input):
    dots, instructions = parse_input(input)

    print(dots)
    print(instructions)

    for instruction in instructions:
        for index, dot in enumerate(dots):
            x, y = dot
            direction, value = instruction
            if direction == "y":
                if y > value:
                    dots[index] = (x, value-(y-value))
            if direction == "x":
                if x > value:
                    dots[index] = (value-(x-value), y)

    for y in range(6):
        line = ["#" if ((x, y) in dots) else "." for x in range(42)]
        print("".join(line))

    return "See above..."


@advent.command()
def test():
    test_input = [
        "6,10",
        "0,14",
        "9,10",
        "0,3",
        "10,4",
        "4,11",
        "6,0",
        "6,12",
        "4,1",
        "0,13",
        "10,12",
        "3,4",
        "3,0",
        "8,4",
        "1,10",
        "2,14",
        "8,10",
        "9,0",
        "",
        "fold along y=7",
        "fold along x=5"
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
