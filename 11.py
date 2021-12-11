import click
from aocd import lines
from aocd import submit as aocd_submit

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version="0.0.1")
def advent():
    pass


def parse_input(map_lines):
    map = {}
    for y, map_line in enumerate(map_lines):
        for x, n in enumerate(map_line):
            map[(x, y)] = int(n)

    return map, len(map_lines[0]), len(map_lines)


def print_map(map, width, height):
    print("#"*10)
    for y in range(height):
        print("".join([str(map[(x, y)]) for x in range(width)]))


def simulate_step(map, width, height):
    flashed = []
    to_flash = []

    print_map(map, width, height)

    for m, v in map.items():
        map[m] = v + 1

        if map[m] > 9:
            to_flash.append(m)

    while(to_flash):
        for flash in to_flash:
            x, y = flash
            consider = [
                (x, y-1),
                (x, y+1),
                (x-1, y),
                (x+1, y),
                (x+1, y+1),
                (x-1, y-1),
                (x+1, y-1),
                (x-1, y+1)
            ]

            for con in consider:
                if con in map and con not in flashed:
                    map[con] += 1

            map[flash] = 0
            flashed.append(flash)

        to_flash = [m for m, v in map.items() if map[m] > 9]

    return len(flashed)


def a_solver(input):
    map, width, height = parse_input(input)

    flashes = 0

    for _ in range(100):
        flashes += simulate_step(map, width, height)

    return flashes


def b_solver(input):
    map, width, height = parse_input(input)

    flashes = 0

    for step in range(2000):
        step_flashes = simulate_step(map, width, height)
        print(step, step_flashes, width*height)
        if step_flashes == width*height:
            print("EVERYBODY FLASH NOW")
            return step + 1


@advent.command()
def test():
    test_input = [
        "5483143223",
        "2745854711",
        "5264556173",
        "6141336146",
        "6357385478",
        "4167524645",
        "2176841721",
        "6882881134",
        "4846848554",
        "5283751526"
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
