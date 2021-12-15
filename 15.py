import click
from aocd import lines
from aocd import submit as aocd_submit

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version="0.0.1")
def advent():
    pass


class node:
    def __init__(self, visited, distance, weight):
        self.visited = visited
        self.distance = int(distance)
        self.weight = int(weight)

    def __repr__(self):
        if self.visited:
            return f'({self.weight})'
        else:
            return f' {self.weight} '
    # def __repr__(self):
    #     if self.visited:
    #         return f'({self.distance}  )'
    #     else:
    #         return f' {self.distance}   '


def parse_input(map_lines):
    map = {}
    for y, map_line in enumerate(map_lines):
        for x, n in enumerate(map_line):
            map[(x, y)] = node(False, 9999999999, n)

    map[(0, 0)].distance = 0

    return map, len(map_lines[0]), len(map_lines)


def a_solver(input):
    map, width, height = parse_input(input)

    for y in range(height):
        #line = ["#" if ((x, y) in dots) else "." for x in range(42)]
        line = [str(map[(x, y)]) for x in range(width)]
        print("".join(line))

    target = (width - 1, height - 1)

    print("target:", target, map[target])
    #print(unvisited)

    while not map[target].visited:
        possible_keys = [k for k, node in map.items() if not node.visited]
        print("keys", len(possible_keys))
        min_key = min(possible_keys, key=lambda x: map[x].distance)

        map[min_key].visited = True

        x, y = min_key
        neighbors = [
            (x, y+1),
            (x, y-1),
            (x+1, y),
            (x-1, y)
        ]

        for n in neighbors:
            if n in map:
                dist = map[min_key].distance + map[n].weight
                if dist < map[n].distance:
                    map[n].distance = dist

        # for y in range(height):
        #     #line = ["#" if ((x, y) in dots) else "." for x in range(42)]
        #     line = [str(map[(x, y)]) for x in range(width)]
        #     print("".join(line))

    return map[target].distance


def b_solver(input):
    map, width, height = parse_input(input)

    for x in range(width):
        for y in range(height):
            for a in range(5):
                for b in range(5):
                    risk_level = map[(x, y)].weight + a + b
                    if risk_level > 9:
                        risk_level -= 9
                    map[(x+(a*width), y+(b*height))] = node(False, 9999999999, risk_level)

    map[(0, 0)].distance = 0
    width = width * 5
    height = height * 5

    target = (width - 1, height - 1)

    print("target:", target, map[target])

    unvisited = set([
            (0, 0)]
        )

    while len(unvisited) > 0:
        min_key = min(unvisited, key=lambda x: map[x].distance)

        if min_key == target:
            return map[target].distance

        x, y = min_key
        neighbors = [
            (x, y+1),
            (x, y-1),
            (x+1, y),
            (x-1, y)
        ]

        for n in neighbors:
            if n in map and not map[n].visited:
                unvisited.add(n)
                dist = map[min_key].distance + map[n].weight
                if dist < map[n].distance:
                    map[n].distance = dist

        map[min_key].visited = True
        unvisited.remove(min_key)
        print("Unvisited: ", min_key, len(unvisited))
    return map[target].distance


@advent.command()
def test():
    test_input = [
        "1163751742",
        "1381373672",
        "2136511328",
        "3694931569",
        "7463417111",
        "1319128137",
        "1359912421",
        "3125421639",
        "1293138521",
        "2311944581"
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
