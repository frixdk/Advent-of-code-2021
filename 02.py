
import click
from aocd import lines
from aocd import submit as aocd_submit

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version="0.0.1")
def advent():
    pass


def a_solver(input):
    position = 0
    depth = 0

    def up(unit):
        nonlocal depth
        depth -= unit

    def down(unit):
        nonlocal depth
        depth += unit

    def forward(unit):
        nonlocal position
        position += unit

    commands = {
        "up": up,
        "down": down,
        "forward": forward
    }

    for command, unit in [x.split() for x in input]:
        commands.get(command)(int(unit))

    return position * depth


def b_solver(input):
    position = 0
    depth = 0
    aim = 0

    def up(unit):
        nonlocal aim
        aim -= unit

    def down(unit):
        nonlocal aim
        aim += unit

    def forward(unit):
        nonlocal position, depth
        position += unit
        depth += aim * unit

    commands = {
        "up": up,
        "down": down,
        "forward": forward
    }

    for command, unit in [x.split() for x in input]:
        commands.get(command)(int(unit))

    return position * depth


@advent.command()
def test():
    test_input = [
        "forward 5",
        "down 5",
        "forward 8",
        "up 3",
        "down 8",
        "forward 2"]
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
