from typing import Union, Optional
from copy import deepcopy
import itertools
import functools

task = '13'
TEST="""[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]""".split("\n")
Packets = Union[list['Packets'], int]
Pair = tuple[Packets, Packets]


def load_lines() -> list[str]:
	lines = []
	with open(f"{task}.in") as file:
		while line := file.readline():
			lines.append(line.rstrip())
	return lines



def parse_lines(lines: list[str]) -> list[Pair]:
	pairs: list[Pair] = []
	for index in range(0, len(lines), 3):
		first: Packets = parse_line(lines[index])[0]
		second: Packets = parse_line(lines[index + 1])[0]
		pair = first, second
		pairs.append(pair)
	return pairs


def parse_line(line: str) -> tuple[Packets, str]:
	assert line[0] == '['
	packets: Packets = []
	line = line[1:]
	while line:
		if line[0] == '[':
			inner, line = parse_line(line)
			packets.append(inner)
		elif line[0] == ']':
			return packets, line[1:]
		elif line[0] == ',':
			line = line[1:]
		else:
			until = min([
				line.index(',') if ',' in line else len(line),
				line.index(']') if ']' in line else len(line)
			])
			num = int(line[:until])
			packets.append(num)
			line = line[until:]
	raise "Invalid line"


def is_in_right_order(pair: Pair) -> Optional[bool]:
	first, second = pair
	for index in range(len(first)):
		left = first[index]
		if index == len(second):
			# Right out of items -> incorrect order
			return False
		right = second[index]
		# Both integers -> compare
		if isinstance(left, int) and isinstance(right, int):
			if left == right:
				continue
			elif left < right:
				return True
			else:
				return False
		# One is list -> deep compare
		left = left if isinstance(left, list) else [left]
		right = right if isinstance(right, list) else [right]
		new_pair = left, right
		result = is_in_right_order(new_pair)
		if result is None:
			continue
		else:
			return result

	# Went through all items -> inconclusive
	if len(first) == len(second):
		return None
	# Left out of items -> correct order
	return True


def first_part(input: list[Pair]) -> int:
	sum = 0
	for index, pair in enumerate(input):
		if is_in_right_order(pair):
			sum += index + 1
	return sum


def cmp_packets(first: Packets, second: Packets) -> int:
	pair = first, second
	result = is_in_right_order(pair)
	if result is None:
		return 0
	elif result:
		return 1
	else:
		return -1


def second_part(input: list[Pair]) -> int:
	dividers = parse_lines(["[[2]]", "[[6]]"])
	input.extend(dividers)
	all_packets = list(itertools.chain(*input))
	all_packets.sort(key=functools.cmp_to_key(cmp_packets), reverse=True)
	return (all_packets.index(dividers[0][0]) + 1) * (all_packets.index(dividers[0][1]) + 1)


if __name__ == '__main__':
	input = parse_lines(TEST)
	input = parse_lines(load_lines())
	first = first_part(deepcopy(input))
	print(f"First part: {first}")
	second = second_part(deepcopy(input))
	print(f"First part: {second}")
