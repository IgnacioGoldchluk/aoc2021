from typing import List
from io import StringIO
from functools import reduce


class Packet:
    def __init__(self, version: int, type_id: int):
        self.version: int = version
        self.type_id: int = type_id
        self.contents: str = ""
        self.length_type_id: int = -1
        self.packets: List[Packet] = []

    def get_value(self) -> int:
        if self.type_id == 4:
            return int(self.contents, 2)
        if self.type_id == 0:
            return sum(packet.get_value() for packet in self.packets)
        if self.type_id == 1:
            return reduce(lambda accum, packet: accum * packet.get_value(), self.packets, 1)
        if self.type_id == 2:
            return min(packet.get_value() for packet in self.packets)
        if self.type_id == 3:
            return max(packet.get_value() for packet in self.packets)
        if self.type_id == 5:
            return int(self.packets[0].get_value() > self.packets[1].get_value())
        if self.type_id == 6:
            return int(self.packets[0].get_value() < self.packets[1].get_value())
        if self.type_id == 7:
            return int(self.packets[0].get_value() == self.packets[1].get_value())


def get_input(filename: str) -> str:
    with open(filename, "r") as f:
        contents = f.read()
    return contents.strip()


def hex_to_bin(hex_string: str) -> str:
    return "".join("{:04b}".format(int(hex_num, 16)) for hex_num in hex_string)


def parse_contents(stream: StringIO) -> str:
    signal = "1"
    values = []
    while signal != "0":
        signal = stream.read(1)
        values.append(stream.read(4))
    return "".join(values)


def add_version_number(packet: Packet) -> int:
    return packet.version + sum(add_version_number(pkt) for pkt in packet.packets)


def parse_stream(stream: StringIO) -> Packet:
    version = int(stream.read(3), 2)
    type_id = int(stream.read(3), 2)
    packet = Packet(version, type_id)

    if type_id != 4:
        packet.length_type_id = int(stream.read(1), 2)
        if packet.length_type_id == 0:
            bits_length = int(stream.read(15), 2)
            start = stream.tell()
            while stream.tell() != start + bits_length:
                packet.packets.append(parse_stream(stream))
        elif packet.length_type_id == 1:
            expected_packets_length = int(stream.read(11), 2)
            while len(packet.packets) != expected_packets_length:
                packet.packets.append(parse_stream(stream))
    else:
        packet.contents = parse_contents(stream)

    return packet


if __name__ == "__main__":
    hex_string = get_input("aoc_2021/2021_16.txt")
    binary_stream = StringIO(hex_to_bin(hex_string))
    packet = parse_stream(binary_stream)
    print(add_version_number(packet))
    print(packet.get_value())
