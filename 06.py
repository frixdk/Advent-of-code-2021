from collections import defaultdict

import click
from aocd import data
from aocd import submit as aocd_submit

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version="0.0.1")
def advent():
    pass


def parse_input(input):
    fish = defaultdict(int)
    for i in [int(i) for i in input.split(",")]:
        fish[i] += 1

    return fish


def solver(input, days):
    fish = parse_input(input)

    for i in range(days):
        fish = simulate_day(fish)
        print(i+1, sum(fish.values()))

    return sum(fish.values())


def simulate_day(fish):
    return {
        0: fish[1],
        1: fish[2],
        2: fish[3],
        3: fish[4],
        4: fish[5],
        5: fish[6],
        6: fish[7] + fish[0],
        7: fish[8],
        8: fish[0],
    }


def a_solver(input):
    return solver(input, 80)


def b_solver(input):
    return solver(input, 256)


@advent.command()
def test():
    test_input = "3, 4, 3, 1, 2"

    print("A result:", a_solver(test_input))
    print("B result:", b_solver(test_input))


@advent.command()
def solve():
    print("A result:", a_solver(data))
    print("B result:", b_solver(data))


@advent.command()
def submit():
    aocd_submit(a_solver(data), part="a")
    aocd_submit(b_solver(data), part="b")


if __name__ == "__main__":
    advent()
