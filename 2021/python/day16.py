from math import prod
from dataclasses import dataclass
from typing import List, Dict, Tuple

from utils import get_input_text

EXAMPLE_INPUT = '''\
C200B40A82
'''
# EXPECTED_1 = 14
# EXPECTED_2 = 3


def get_input_data(example=False) -> None:
    if example:
        input_text = EXAMPLE_INPUT
    else:
        input_text = get_input_text(16)
    return input_text.strip()


@dataclass
class Packet:
    version: int
    type_id: str
    body: str


input_data = get_input_data(True)


def _create_packet(packet: str) -> Tuple[int, str, str]:
    version = int(packet[:3], 2)
    type_id = packet[3:6]
    body = packet[6:]
    return Packet(version=version, type_id=type_id, body=body)



def analyze_packet(packet: str) -> Tuple[int, int]:
    packet = _create_packet(packet)
    header_bits = 6
    sum_of_versions = packet.version

    if packet.type_id == '100':
        current_index = 0
        first_char = packet.body[current_index]
        literal_number = ''
        # 10101 10010 01001
        while first_char == '1':
            literal_number += packet.body[current_index + 1:current_index + 5]
            current_index += 5
            first_char = packet.body[current_index]
        # last number
        literal_number += packet.body[current_index + 1:current_index + 5]
        # sum offset = header + end of 5-bit numbers
        packet_total_length = header_bits + current_index + 5
        value = int(literal_number, 2)
    else:
        sub_packet_values = []
        length_type_id = packet.body[0]
        # first bit of body is length type id
        if length_type_id == '0':
            # next 15 bits are total sub packets length
            # next sub_packets_length bits is the length of the sub packets
            sub_packets_length = int(packet.body[1:16], 2)
            sub_packets = packet.body[16:]
            index = 0
            while index < sub_packets_length:
                ver, o, val = analyze_packet(sub_packets)
                sum_of_versions += ver
                sub_packets = sub_packets[o:]
                sub_packet_values.append(val)
                index += o
            packet_total_length = sub_packets_length + 15 + 1 + header_bits
        else:
            # next 11 bits show the number of sub packets
            # unknow number of bits for sub packets
            number_of_subs = int(packet.body[1:12], 2)
            sub_packets = packet.body[12:]
            index = 0
            for _ in range(number_of_subs):
                ver, o, val = analyze_packet(sub_packets)
                sum_of_versions += ver
                sub_packets = sub_packets[o:]
                sub_packet_values.append(val)
                index += o
            packet_total_length = index + 11 + 1 + header_bits

        # find value
        if packet.type_id == '000':
            value = sum(sub_packet_values)
        elif packet.type_id == '001':
            value = prod(sub_packet_values)
        elif packet.type_id == '010':
            value = min(sub_packet_values)
        elif packet.type_id == '011':
            value = max(sub_packet_values)
        elif packet.type_id == '101':
            value = int(sub_packet_values[0] > sub_packet_values[1])
        elif packet.type_id == '110':
            value = int(sub_packet_values[0] < sub_packet_values[1])
        elif packet.type_id == '111':
            value = int(sub_packet_values[0] == sub_packet_values[1])

    return sum_of_versions, packet_total_length, value



def solve_1() -> int:
    packet = bin(int(input_data, 16))[2:].zfill(len(input_data) * 4)
    sum_of_versions, *_ = analyze_packet(packet)
    return sum_of_versions


def solve_2() -> int:
    packet = bin(int(input_data, 16))[2:].zfill(len(input_data) * 4)
    *_, value = analyze_packet(packet)
    return value


def solve():
    part_1 = solve_1()
    print(f'Part 1: {part_1}')

    part_2 = solve_2()
    print(f'Part 2: {part_2}')


if __name__ == '__main__':
    solve()
