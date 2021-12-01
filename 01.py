
import click
from aocd import data, lines, numbers
from aocd import submit as aocd_submit

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version="0.0.1")
def advent():
    pass


def a_solver(input):
    increases = 0
    for index, i in enumerate(input):
        if index > 0 and i > input[index-1]:
            increases += 1

    return increases


def b_solver(input):
    windows = [i + input[index + 1] + input[index + 2] for index, i in enumerate(input[:-2])]

    return a_solver(windows)


@advent.command()
def test():
    test_input = [
        199,
        200,
        208,
        210,
        200,
        207,
        240,
        269,
        260,
        263]
    print("A result:", a_solver(test_input))
    print("B result:", b_solver(test_input))


@advent.command()
def solve():
    print("A result:", a_solver(numbers))
    print("B result:", b_solver(numbers))


@advent.command()
def submit():
    aocd_submit(a_solver(numbers), part="a")
    aocd_submit(b_solver(numbers), part="b")


if __name__ == "__main__":
    advent()
