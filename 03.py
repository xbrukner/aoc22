from functools import reduce
from typing import Iterator, TypeVar
from itertools import islice
import operator

task = '03'

Compartments = tuple[str, str]
Input = list[str]


def line_to_compartments(line: str) -> Compartments:
	mid = int(len(line) / 2)
	return line[0:mid], line[mid:]


def load_input() -> Input:
	result: Input = []
	with open(f"{task}.in") as file:
		while line := file.readline().rstrip():
			result.append(line)
	return result


def common(compartments: Compartments) -> str:
	return ({*compartments[0]} & ({*compartments[1]})).pop()


def priority(letter: str) -> int:
	return ord(letter) - (ord('a') - 1 if "a" <= letter <= "z" else ord('A') - 27)


def first_part(inp: Input) -> int:
	return sum([priority(common(line_to_compartments(line))) for line in inp])


# Part 2
T = TypeVar('T')


# Adapted from https://stackoverflow.com/a/312464
def chunk(lst: list[T], size: int) -> Iterator[list[T]]:
	for i in range(0, len(lst), size):
		yield lst[i:i + size]


def common_lines(lines: islice) -> str:
	return reduce(operator.and_, [{*line} for line in lines]).pop()


def second_part(inp: Input) -> int:
	return sum([priority(common_lines(chunks)) for chunks in chunk(inp, 3)])


if __name__ == '__main__':
	inp = load_input()
	first = first_part(inp)
	print(f"First part: {first}")
	second = second_part(inp)
	print(f"Second part: {second}")
