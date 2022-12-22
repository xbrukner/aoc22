task = '18'
TEST = """2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5""".split('\n')

Coords = tuple[int, int, int]
Map = set[Coords]


def load_file() -> list[str]:
	lines = []
	with open(f"{task}.in") as file:
		while line := file.readline().rstrip():
			lines.append(line)
	return lines


def parse_line(line: str) -> Coords:
	return tuple([int(num) for num in line.split(',')])


def parse_map(input: list[str]) -> Map:
	return {parse_line(line) for line in input}


def add_coords(first: Coords, second: Coords) -> Coords:
	return first[0] + second[0], first[1] + second[1], first[2] + second[2]


def within_bounds(cube: Coords, minimum: Coords, maximum: Coords) -> bool:
	return minimum[0] <= cube[0] <= maximum[0] and \
		minimum[1] <= cube[1] <= maximum[1] and \
		minimum[2] <= cube[2] <= maximum[2]


RELATIVE = [(0, 0, 1), (0, 0, -1), (0, 1, 0), (0, -1, 0), (1, 0, 0), (-1, 0, 0)]


def connected(coord: Coords, map: Map) -> list[Coords]:
	return [r for r in RELATIVE if add_coords(coord, r) in map]


def first_part(map: Map) -> int:
	return sum([6 - len(connected(cube, map)) for cube in map])


def fill(lava: Map, map: Map, minimum: Coords, maximum: Coords, cube: Coords):
	stack = [cube]
	while stack:
		cube = stack[0]
		if cube in lava:
			stack.pop(0)
			continue
		lava.add(cube)
		options = [cube for cube in [add_coords(cube, r) for r in RELATIVE]
				   if within_bounds(cube, minimum, maximum) and cube not in lava and cube not in map
				   ]

		stack.extend(options)
		stack.pop(0)


def second_part(map: Map) -> int:
	minimum = [min([cube[i] for cube in map]) - 1 for i in range(3)]
	maximum = [max([cube[i] for cube in map]) + 1 for i in range(3)]

	lava: Map = set()
	fill(lava, map, minimum, maximum, tuple(minimum))

	return sum([len(connected(cube, lava)) for cube in map])


if __name__ == '__main__':
	map = parse_map("""1,1,1\n2,1,1""".split('\n'))
	map = parse_map(TEST)
	map = parse_map(load_file())
	first = first_part(map)
	print(f'First part: {first}')
	second = second_part(map)
	print(f'Second part: {second}')
