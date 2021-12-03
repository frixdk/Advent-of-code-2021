import copy

import click
from aocd import lines
from aocd import submit as aocd_submit

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version="0.0.1")
def advent():
    pass


def a_solver(input):
    gamma_bits = []
    epsilon_bits = []

    for bits in zip(*input):
        if len([b for b in bits if b == "1"]) > len(bits) / 2:
            gamma_bits.append("1")
            epsilon_bits.append("0")
        else:
            gamma_bits.append("0")
            epsilon_bits.append("1")

    gamma_rate = int("".join(gamma_bits), 2)
    epsilon_rate = int("".join(epsilon_bits), 2)

    return gamma_rate * epsilon_rate


def b_solver(org_input):
    input = copy.copy(org_input)
    print(input)
    for index in range(len(input[0])):
        bits = list(zip(*input))[index]
        if len([b for b in bits if b == "1"]) >= len(bits) / 2:
            input = [n for n in input if n[index] == '1']
        else:
            input = [o for o in input if o[index] == '0']

        if len(input) == 1:
            break

    oxygen = int(input[0], 2)

    input = copy.copy(org_input)
    for index in range(len(input[0])):
        bits = list(zip(*input))[index]
        if len([b for b in bits if b == "1"]) < len(bits) / 2:
            input = [n for n in input if n[index] == '1']
        else:
            input = [o for o in input if o[index] == '0']

        if len(input) == 1:
            break

    co2 = int(input[0], 2)

    return oxygen * co2

@advent.command()
def test():
    test_input = [
        "00100",
        "11110",
        "10110",
        "10111",
        "10101",
        "01111",
        "00111",
        "11100",
        "10000",
        "11001",
        "00010",
        "01010",
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
