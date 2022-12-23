from typing import Callable, Optional
from dataclasses import dataclass, field
task = '22'
TEST="""        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5""".split("\n")


@dataclass
class Item:
	movements: Optional[int] = field(default=None)
	direction: Optional[str] = field(default=None)


Coord = tuple[int, int]
Map = dict[Coord, str]
Directions = list[Item]


def load_file() -> list[str]:
	lines = []
	with open(f'{task}.in') as file:
		while line := file.readline():
			lines.append(line.rstrip())
	return lines


def load_map(input: list[str]) -> Map:
	map = {}
	for y, line in enumerate(input):
		for x, str in enumerate(line):
			if str != ' ':
				map[(x + 1), (y + 1)] = str
	return map


def load_directions(input: str) -> Directions:
	directions = []
	while input:
		next = len(input)
		if 'L' in input:
			next = min(next, input.index('L'))
		if 'R' in input:
			next = min(next, input.index('R'))
		directions.append(Item(movements=int(input[:next])))
		if 'L' in input or 'R' in input:
			directions.append(Item(direction=input[next]))
			input = input[next + 1:]
		else:
			return directions
	return directions


def load_input(input: list[str]) -> tuple[Map, Directions]:
	return load_map(input[:-2]), load_directions(input[-1])


Vector = tuple[int, int]
movements: list[Vector] = [(1, 0), (0, 1), (-1, 0), (0, -1)] # right, down, left, up


def step(coord: Coord, direction: int) -> Coord:
	return coord[0] + movements[direction][0], coord[1] + movements[direction][1]


def wrap(coord: Coord, map: Map, direction: int) -> Coord:
	opposite = (direction + 2) % 4
	while (moved := step(coord, opposite)) in map:
		coord = moved
	return coord


def move(coord: Coord, map: Map, direction: int, wrap: Callable[[Coord, int], tuple[Coord, int]]) -> tuple[Coord, int]:
	moved = step(coord, direction)
	if moved in map:
		if map[moved] == '.':
			return moved, direction
		else:
			return coord, direction
	else:
		wrapped, new_direction = wrap(coord, direction)
		if wrapped in map:
			if map[wrapped] == '.':
				return wrapped, new_direction
			else:
				return coord, direction


def find_start(map: Map) -> Coord:
	x = 1
	while (x, 1) not in map:
		x += 1
	return x, 1


def first_part(input: tuple[Map, Directions]) -> int:
	map, directions = input
	pos = find_start(map)
	facing = 0 # Right
	for item in directions:
		if item.movements:
			for _ in range(item.movements):
				pos, facing = move(pos, map, facing, lambda coord, direction: (wrap(coord, map, direction), direction))
		else:
			facing = (facing + (1 if item.direction == 'R' else -1)) % 4
	return 4 * pos[0] + 1000 * pos[1] + facing


Seam = tuple[Coord, int]
Seams = dict[Coord, dict[Coord, Seam]]
PairWithVector = tuple[Coord, Coord, int]
Corner = tuple[PairWithVector, PairWithVector]


def direction_from_vector(first: Coord, second: Coord) -> int:
	diff = second[0] - first[0], second[1] - first[1]
	return movements.index(diff)


clockwise_circle: list[Coord] = [(0, 0), (1, 0), (1, 1), (0, 1)]
def counter_index(index: int) -> int:
	return (index - 1) % 4
def clockwise_index(index: int) -> int:
	return (index + 1) % 4
def opposite_index(index: int) -> int:
	return (index + 2) % 4
def counter_direction(direction: int) -> int:
	return (direction - 1) % 4
def clockwise_direction(direction: int) -> int:
	return (direction + 1) % 4
def opposite_direction(direction: int) -> int:
	return (direction + 2) % 4


def find_corner(size: int, map: Map) -> list[Corner]:
	result = []
	for x in range(4):
		for y in range(4):
			corners = [(coord[0] + size * x, coord[1] + size * y) for coord in clockwise_circle]
			present = [coord in map for coord in corners]
			if sum(present) == 3:
				missing = present.index(False)
				away = corners[opposite_index(missing)]
				first_in, first_seam = corners[counter_index(missing)], corners[missing]
				second_in, second_seam = corners[clockwise_index(missing)], corners[missing]
				result.append((
					(first_in, first_seam, direction_from_vector(away, first_in)),
					(second_in, second_seam, direction_from_vector(away, second_in))
				))
	return result


def find_corner_seamed(size: int, map: Map, seams: Seams) -> list[Corner]:
	result = []
	for x in range(4):
		for y in range(4):
			corners = [(coord[0] + size * x, coord[1] + size * y) for coord in clockwise_circle]
			present = [coord in map for coord in corners]
			if sum(present) == 2:
				existing_seams = [coord in seams for coord in corners]
				if sum(existing_seams) == 1:
					seam = existing_seams.index(True)
					missing = [existing_seams[i] or present[i] for i in range(4)].index(False)
					away = corners[opposite_index(missing)]
					seamed_in, seam_direction = seams[corners[seam]][away]
					seamed_away = step(seamed_in, opposite_direction(seam_direction))

					first_in, first_seam, first_away = (corners[counter_index(missing)], corners[missing], away) \
						if seam != counter_index(missing) \
						else (seamed_in, step(seamed_in, clockwise_direction(seam_direction)), seamed_away)
					second_in, second_seam, second_away = (corners[clockwise_index(missing)], corners[missing], away) \
						if seam != clockwise_index(missing) \
						else (seamed_in, step(seamed_in, counter_direction(seam_direction)), seamed_away)
					result.append((
						(first_in, first_seam, direction_from_vector(first_away, first_in)),
						(second_in, second_seam, direction_from_vector(second_away, second_in))
					))
	return result


def seam_corner(size: int, corner: Corner, seams: Seams):
	first, second = corner
	first, first_seam, first_move = first
	second, second_seam, second_move = second
	first_direction = direction_from_vector(first_seam, first)
	second_direction = direction_from_vector(second_seam, second)

	for _ in range(size):
		if first_seam not in seams:
			seams[first_seam] = {}
		seams[first_seam][first] = second, second_direction
		if second_seam not in seams:
			seams[second_seam] = {}
		seams[second_seam][second] = first, first_direction
		first_seam = step(first_seam, first_move)
		first = step(first, first_move)
		second_seam = step(second_seam, second_move)
		second = step(second, second_move)


def wrap_cube(coord: Coord, seams: Seams, direction: int) -> tuple[Coord, int]:
	return seams[step(coord, direction)][coord]


def second_part(input: tuple[Map, Directions]) -> int:
	map, directions = input
	size = 50
	seams = {}
	for corner in find_corner(size, map):
		seam_corner(size, corner, seams)
	while corners := find_corner_seamed(size, map, seams):
		for corner in corners:
			seam_corner(size, corner, seams)
	pos = find_start(map)
	facing = 0 # Right
	for item in directions:
		if item.movements:
			for _ in range(item.movements):
				pos, facing = move(pos, map, facing, lambda coord, direction: wrap_cube(coord, seams, direction))
		else:
			facing = (facing + (1 if item.direction == 'R' else -1)) % 4
	return 4 * pos[0] + 1000 * pos[1] + facing


if __name__ == '__main__':
	input = load_input(TEST)
	input = load_input(load_file())
	first = first_part(input)
	print(f'First part: {first}')
	second = second_part(input)
	print(f'Second part: {second}')
	test = False
	if test:
		seams = {}
		for corners in find_corner(4, input[0]):
			seam_corner(4, corners, seams)
		# <^
		assert wrap_cube((8, 5), seams, 3) == ((9, 4), 0)
		assert wrap_cube((9, 4), seams, 2) == ((8, 5), 1)
		assert wrap_cube((5, 5), seams, 3) == ((9, 1), 0)
		assert wrap_cube((9, 2), seams, 2) == ((6, 5), 1)
		# >v
		assert wrap_cube((12, 6), seams, 0) == ((15, 9), 1)
		assert wrap_cube((14, 9), seams, 3) == ((12, 7), 2)
		# <v
		assert wrap_cube((7, 8), seams, 1) == ((9, 10), 0)
		assert wrap_cube((9, 9), seams, 2) == ((8, 8), 3)
		# v> missing on current map
		for corners in find_corner_seamed(4, input[0], seams):
			seam_corner(4, corners, seams)
		# _^>< -> 4,5; 4,6
		assert wrap_cube((4, 5), seams, 3) == ((9, 1), 1)
		assert wrap_cube((9, 1), seams, 3) == ((4, 5), 1)
		assert wrap_cube((1, 5), seams, 3) == ((12, 1), 1)
		assert wrap_cube((12, 1), seams, 3) == ((1, 5), 1)
		# <>v_ -> 4,8; 4,9
		assert wrap_cube((4, 8), seams, 1) == ((9, 12), 3)
		assert wrap_cube((1, 8), seams, 1) == ((12, 12), 3)
		# <_>v -> 12,4; 12,5
		assert wrap_cube((12, 4), seams, 0) == ((16, 9), 2)
		assert wrap_cube((12, 1), seams, 0) == ((16, 12), 2)