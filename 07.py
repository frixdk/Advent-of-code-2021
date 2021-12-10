import click
from aocd import data
from aocd import submit as aocd_submit

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version="0.0.1")
def advent():
    pass


def parse_input(input):
    return [int(i) for i in input.split(",")]


def solver(input, fuel):
    crabs = parse_input(input)
    spent = []
    for i in range(min(crabs), max(crabs) + 1):
        spent.append(sum([fuel(i, x) for x in crabs]))

    return int(min(spent))


def a_solver(input):
    def fuel(i, x):
        return abs(i-x)

    return solver(input, fuel)


def b_solver(input):
    def fuel(i, x):
        return (abs(i-x)*(abs(i-x)+1))/2

    return solver(input, fuel)


@advent.command()
def test():
    test_input = "16,1,2,0,4,2,7,1,2,14"

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
