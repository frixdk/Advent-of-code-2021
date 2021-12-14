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
    return input[0], [l.split(" -> ")for l in input[2:]]



def a_solver(input):
    template, rules = parse_input(input)

    for step in range(10):
        out = ""

        for idx in range(len(template)-1):
            out += template[idx]
            for rule, insert in rules:
                if rule == template[idx] + template[idx+1]:
                    out += insert


        template = out + template[-1]

    c = sorted(Counter(template).values())

    return c[-1] - c[0]


def b_solver(input):
    template, rules = parse_input(input)

    pairs = defaultdict(int)

    for idx in range(len(template)-1):
        pairs[template[idx] + template[idx+1]] += 1

    for step in range(40):

        new_pairs = defaultdict(int)

        for rule, insert in rules:
            new_pairs[rule[0] + insert] += pairs[rule]
            new_pairs[insert + rule[1]] += pairs[rule]

        pairs = new_pairs

    counts = defaultdict(int)
    counts[template[0]] += 1

    for k,v in pairs.items():
        counts[k[1]] += v

    elements = sorted(counts.values())

    return elements[-1] - elements[0]


@advent.command()
def test():
    test_input = [
        "NNCB",
        " ",
        "CH -> B",
        "HH -> N",
        "CB -> H",
        "NH -> C",
        "HB -> C",
        "HC -> B",
        "HN -> C",
        "NN -> C",
        "BH -> H",
        "NC -> B",
        "NB -> B",
        "BN -> B",
        "BB -> N",
        "BC -> B",
        "CC -> N",
        "CN -> C",
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
