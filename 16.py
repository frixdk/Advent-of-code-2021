import math

import click
import more_itertools as mit
from aocd import lines
from aocd import submit as aocd_submit

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version="0.0.1")
def advent():
    pass


def parse_input(input):
    bits = {
        "0": "0000",
        "1": "0001",
        "2": "0010",
        "3": "0011",
        "4": "0100",
        "5": "0101",
        "6": "0110",
        "7": "0111",
        "8": "1000",
        "9": "1001",
        "A": "1010",
        "B": "1011",
        "C": "1100",
        "D": "1101",
        "E": "1110",
        "F": "1111"
    }
    return "".join([bits[i] for i in input[0]])


class packet:
    def __init__(self, version, type_id, value="", operator="", sub_packets=[]):
        self.version = version
        self.type_id = type_id
        self.value = value
        self.operator = operator
        self.sub_packets = sub_packets

    def __repr__(self):
        return "P:" + self.version + ":" + self.type_id + ":" + (str(int(self.value, 2)) if self.value else "NA") + str(self.sub_packets)

    def get_value(self):
        if self.type_id == "000":
            # sum
            return sum([s.get_value() for s in self.sub_packets])
        if self.type_id == "001":
            # product
            return math.prod([s.get_value() for s in self.sub_packets])
        if self.type_id == "010":
            # min
            return min([s.get_value() for s in self.sub_packets])
        if self.type_id == "011":
            # max
            return max([s.get_value() for s in self.sub_packets])
        if self.type_id == "100":
            # value
            return int(self.value, 2)
        if self.type_id == "101":
            # greater than
            return 1 if self.sub_packets[0].get_value() > self.sub_packets[1].get_value() else 0
        if self.type_id == "110":
            # less than
            return 1 if self.sub_packets[0].get_value() < self.sub_packets[1].get_value() else 0
        if self.type_id == "111":
            # equal to
            return 1 if self.sub_packets[0].get_value() == self.sub_packets[1].get_value() else 0


def parse_packet(bits):
    print("PARSE", bits)
    if not bits or int(bits) == 0:
        return [], len(bits)

    version = bits[:3]
    type_id = bits[3:6]

    size = 6

    if type_id == "100":

        value = ""
        counter = 0
        for number in list(mit.chunked(bits[6:], 5)):
            value += "".join(number[1:])
            counter += 5
            if number[0] == "0":
                break
        size += counter

        return packet(version, type_id, value=value), size

    else:
        mode = bits[6]

        size += 1

        if mode == "0":
            size += 15

            packet_length = int(bits[7:size], 2)

            sub_packets = []
            size_counter = 0

            while size_counter < packet_length:
                sub, inner_size = parse_packet(bits[size+size_counter:])
                sub_packets.append(sub)
                size_counter += inner_size

            size += size_counter
            return packet(version, type_id, sub_packets=sub_packets), size

        else:
            size += 11

            n = int(bits[7:size], 2)

            sub_packets = []
            size_counter = 0

            while(len(sub_packets) < n):
                sub, inner_size = parse_packet(bits[size+size_counter:])
                sub_packets.append(sub)
                size_counter += inner_size

            size += size_counter
            return packet(version, type_id, sub_packets=sub_packets), size


def get_version_sum(packet):

    if packet.sub_packets:
        sub = sum([get_version_sum(p) for p in packet.sub_packets])
        return int(packet.version, 2) + sub
    else:
        return int(packet.version, 2)


def calc_expression(packet):
    return packet.get_value()


def a_solver(input):
    bits = parse_input(input)
    packet, size = parse_packet(bits)
    s = get_version_sum(packet)
    return s


def b_solver(input):
    bits = parse_input(input)
    packet, size = parse_packet(bits)

    print(packet)
    return calc_expression(packet)


@advent.command()
def test():
    test_input = [
        #"D2FE28"
        #"38006F45291200"
        #"EE00D40C823060",
        #"8A004A801A8002F478",
        #"620080001611562C8802118E34",
        #"C0015000016115A2E0802F182340",
        #"A0016C880162017C3686B18A3D4780",

        #"C200B40A82"
        #"04005AC33890"
        #"880086C3E88112"
        #"CE00C43D881120"
        #"D8005AC2A8F0"
        #"F600BC2D8F"
        #"9C005AC2F8F0"
        "9C0141080250320F1802104A08"

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
