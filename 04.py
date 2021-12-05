import click
from aocd import lines
from aocd import submit as aocd_submit

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version="0.0.1")
def advent():
    pass


class field:
    def __init__(self, value):
        self.value = int(value)
        self.marked = False

    def __repr__(self):
        if self.marked:
            return f'({self.value})'
        else:
            return f' {self.value} '


class board:
    def __init__(self, irows):
        self.rows = [[field(n) for n in row] for row in irows]

    def __repr__(self):
        return f'Board rows {self.rows}'

    def print_board(self):
        for row in self.rows:
            print(row)

    def mark(self, number):
        for row in self.rows:
            for field in row:
                if field.value == number:
                    field.marked = True

    def check_winner(self):
        for index in range(len(self.rows)):

            # rows
            if all([field.marked for field in self.rows[index]]):
                return True

            # columns
            if all([row[index].marked for row in self.rows]):
                return True

        return False

    def get_score(self):
        return sum([int(field.value) for row in self.rows for field in row if not field.marked])


def parse_input(input):
    numbers = input[0].split(",")

    boards = []
    board_rows = []

    for line in input[1:]:
        row = line.split()

        if row:
            board_rows.append(row)
        elif board_rows:
            boards.append(board(board_rows))
            board_rows = []

    boards.append(board(board_rows))

    return [int(n) for n in numbers], boards


def a_solver(input):
    numbers, boards = parse_input(input)

    for n in numbers:
        print("number", n)
        for b in boards:
            b.mark(n)

            if b.check_winner():
                b.print_board()
                return b.get_score() * int(n)


def b_solver(input):
    numbers, boards = parse_input(input)

    for n in numbers:
        print("number", n)
        winners = []

        for b in boards:
            b.mark(n)

            if b.check_winner():
                winners.append(b)
                if len(boards) == 1:
                    print("last winner")
                    b.print_board()
                    return b.get_score() * int(n)

        for winner in winners:
            boards.remove(winner)


@advent.command()
def test():
    test_input = [
        "7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1",

        "22 13 17 11  0",
        "8  2 23  4 24",
        "21  9 14 16  7",
        "6 10  3 18  5",
        "1 12 20 15 19",
        "",
        "3 15  0  2 22",
        "9 18 13 17  5",
        "19  8  7 25 23",
        "20 11 10 24  4",
        "14 21 16 12  6",
        "",
        "14 21 17 24  4",
        "10 16 15  9 19",
        "18  8 23 26 20",
        "22 11 13  6  5",
        "2  0 12  3  7"
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
