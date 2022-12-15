import copy
from copy import deepcopy

task = '14'
TEST = """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9""".split("\n")
Position = tuple[int, int] # y, x
Map = dict[Position, str]


def draw_line(map: Map, first: Position, second: Position):
	if first[0] == second[0]: # horizontal
		start = min(first[1], second[1])
		end = max(first[1], second[1])
		for x in range(start, end + 1):
			map[(first[0], x)] = '#'
	else: # vertical
		start = min(first[0], second[0])
		end = max(first[0], second[0])
		for y in range(start, end + 1):
			map[(y, first[1])] = '#'


def parse_position(input: str) -> Position:
	y, x = input.rstrip().split(',')
	return int(y), int(x)


def parse_input(lines: list[str]) -> Map:
	map: Map = {}
	for line in lines:
		positions = line.split('->')
		for index in range(len(positions) - 1):
			first = parse_position(positions[index])
			second = parse_position(positions[index + 1])
			draw_line(map, first, second)
	return map


def read_input() -> list[str]:
	lines = []
	with open(f"{task}.in") as file:
		while line := file.readline():
			lines.append(line)
	return lines


def lowest_line(map: Map) -> int:
	return max(key[1] for key in map.keys())


def add_sand(map: Map, limit: int) -> tuple[bool, Position]:
	x = 500
	for y in range(0, limit + 1):
		if (x, y) in map: # found obstacle
			if (x - 1, y) not in map: # try moving left
				x -= 1
				continue
			if (x + 1, y) not in map: # try moving right
				x += 1
				continue
			# stop one line above
			map[(x, y - 1)] = 'o'
			return False, (x, y - 1)
	return True, (x, y)


def first_part(map: Map) -> int:
	limit = lowest_line(map)
	count = 0
	while not add_sand(map, limit)[0]:
		count += 1
	return count


def second_part(map: Map) -> int:
	limit = lowest_line(map)
	draw_line(map, (500 - limit - 3, limit + 2), (500 + limit + 3, limit + 2))
	count = 0
	while add_sand(map, limit + 3)[1] != (500, 0):
		count += 1
	return count + 1



if __name__ == '__main__':
	map = parse_input(TEST)
	map = parse_input(read_input())
	first = first_part(copy.deepcopy(map))
	print(f"First part: {first}")
	second = second_part(copy.deepcopy(map))
	print(f"Second part: {second}")

