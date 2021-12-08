from collections import defaultdict
from aocd.transforms import lines

import click
from aocd import lines
from aocd import submit as aocd_submit

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version="0.0.1")
def advent():
    pass


def parse_input(input):
    return [(i.split(" | ")[0].split(), i.split(" | ")[1].split()) for i in input]
    #return patterns.split(), output.split()


def solver(input, fuel):
    crabs = parse_input(input)
    spent = []
    for i in range(min(crabs), max(crabs) + 1):
        spent.append(sum([fuel(i, x) for x in crabs]))

    return int(min(spent))


def a_solver(input):
    patterns = parse_input(input)
    count = 0
    for p in patterns:
        count += len([f for f in p[1] if len(f) in [2, 3, 4, 7]])

    return count


def b_solver(input):
    patterns = parse_input(input)
    count = 0
    for p in patterns:
        
        digits = {
                1: [f for f in p[0] if len(f) == 2][0],
                7: [f for f in p[0] if len(f) == 3][0],
                4: [f for f in p[0] if len(f) == 4][0],
                8: [f for f in p[0] if len(f) == 7][0]
            }

        for s in [f for f in p[0] if len(f) == 6]:
            if len(set(s)-set(digits[1])) == 5:
                digits[6] = s

        for s in [f for f in p[0] if len(f) == 5]:
            if len(set(s)-set(digits[1])) == 3:
                digits[3] = s

        for s in [f for f in p[0] if len(f) == 6 and f != digits[6]]:
            if len(set(s)-set(digits[4])) == 2:
                digits[9] = s
            else:
                digits[0] = s

        for s in [f for f in p[0] if len(f) == 5 and f != digits[3]]:
            if len(set(s)-set(digits[6])) == 1:
                digits[2] = s
            else:
                digits[5] = s

        output_digits = []
        for x in p[1]:
            for d, s in digits.items():
                if set(x) == set(s):
                    output_digits.append(str(d))

        count += int("".join(output_digits))
        
    return count


@advent.command()
def test():
    test_input = [
        "be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe",
        "edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc",
        "fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg",
        "fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb",
        "aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea",
        "fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb",
        "dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe",
        "bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef",
        "egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb",
        "gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce"
    ]

    #test_input = ["acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf"]

    print("A result:", a_solver(test_input))
    print("B result:", b_solver(test_input))


@advent.command()
def solve():
    print("bab", lines)
    print("A result:", a_solver(lines))
    print("B result:", b_solver(lines))


@advent.command()
def submit():
    aocd_submit(a_solver(lines), part="a")
    aocd_submit(b_solver(lines), part="b")


if __name__ == "__main__":
    advent()
