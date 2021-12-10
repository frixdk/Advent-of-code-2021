import click
from aocd import lines
from aocd import submit as aocd_submit

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version="0.0.1")
def advent():
    pass


def parse_input(chunk_lines):
    return [[c for c in chunk] for chunk in chunk_lines]


CLOSES = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">"
}

POINTS = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137
}


def solver(input):
    chunks = parse_input(input)

    score = 0
    completions = []

    for chunk in chunks:
        active = []
        for c in chunk:
            if c in CLOSES.keys():
                active.append(c)
            elif CLOSES[active[-1]] == c:
                active.pop(-1)
            else:
                #print(f"Syntax Error. Expected {active[-1]}, but found {c} instead")
                score += POINTS[c]
                active = []
                break

        if active:
            complete = [CLOSES[a] for a in active]
            complete.reverse()
            completions.append(complete)

    return score, completions


def a_solver(input):
    score, _ = solver(input)
    return score


def b_solver(input):
    _, completions = solver(input)

    com_points = {
        ")": 1,
        "]": 2,
        "}": 3,
        ">": 4
    }

    scores = []
    for completion in completions:
        score = 0
        for c in completion:
            score = score * 5
            score += com_points[c]

        scores.append(score)

    return sorted(scores)[int(len(scores)/2)]


@advent.command()
def test():
    test_input = [
        "[({(<(())[]>[[{[]{<()<>>",
        "[(()[<>])]({[<{<<[]>>(",
        "{([(<{}[<>[]}>{[]{[(<()>",
        "(((({<>}<{<{<>}{[]{[]{}",
        "[[<[([]))<([[{}[[()]]]",
        "[{[{({}]{}}([{[{{{}}([]",
        "{<[[]]>}<{[{[{[]{()[[[]",
        "[<(<(<(<{}))><([]([]()",
        "<{([([[(<>()){}]>(<<{{",
        "<{([{{}}[<[[[<>{}]]]>[]]"
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
