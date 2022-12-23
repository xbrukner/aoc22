from typing import Optional
task = '23'
TEST = """....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#..""".split('\n')
TEST2 = """.....
..##.
..#..
.....
..##.
.....""".split('\n')

Coord = tuple[int, int]
Map = set[Coord]


def map_get(map: Map, coord: Coord) -> str:
	return map.get(coord, default='.')


def load_file() -> list[str]:
	lines = []
	with open(f'{task}.in') as file:
		while line := file.readline():
			lines.append(line.rstrip())
	return lines


def load_input(lines: list[str]) -> Map:
	map = set()
	for y, line in enumerate(lines):
		for x, s in enumerate(line):
			if s == '#':
				map.add((x, y))
	return map


# Directions:
# y goes down, x goes right
# NW N NE
# W  0  E
# SW S SE
RelativeCoord = tuple[int, int]
Sectors = list[RelativeCoord] # The middle one is always the step
sectors: list[Sectors] = [
	[(-1, -1), (0, -1), (1, -1)], # north (NW, NE)
	[(-1, 1), (0, 1), (1, 1)], # south (SW, SE)
	[(-1, -1), (-1, 0), (-1, 1)], # west (NW, SW)
	[(1, -1), (1, 0), (1, 1)] # east (NE, SE)
]
def add_coord(coord: Coord, rel: RelativeCoord) -> Coord:
	return coord[0] + rel[0], coord[1] + rel[1]


def propose_movement(elf: Coord, start: int, map: Map) -> Optional[Coord]:
	around = any([add_coord(elf, relative) in map
	              for sector in sectors
	              for relative in sector
	])
	if not around:
		return None
	for s in range(4):
		sector = sectors[(start + s) % 4]
		if all([add_coord(elf, relative) not in map for relative in sector]):
			return add_coord(elf, sector[1])


# Or group by count > 1
def find_duplicates(options: dict[Coord, Optional[Coord]]) -> set[Coord]:
	found: set[Coord] = set()
	duplicates: set[Coord] = set()
	for coord in options.values():
		if coord:
			if coord in found:
				duplicates.add(coord)
			found.add(coord)
	return duplicates


def first_part(map: Map) -> int:
	for r in range(10):
		options = {elf: propose_movement(elf, r, map) for elf in map}
		duplicates = find_duplicates(options)
		map = {movement if movement and movement not in duplicates else elf
		       for elf, movement in options.items()}
	min_x = min(c[0] for c in map)
	min_y = min(c[1] for c in map)
	max_x = max(c[0] for c in map)
	max_y = max(c[1] for c in map)
	return (max_x - min_x + 1) * (max_y - min_y + 1) - len(map)


def second_part(map: Map) -> int:
	r = 0
	new_map = set()
	while r == 0 or not map == new_map:
		map = new_map if r else map
		options = {elf: propose_movement(elf, r, map) for elf in map}
		duplicates = find_duplicates(options)
		new_map = {movement if movement and movement not in duplicates else elf
		           for elf, movement in options.items()}
		r += 1
	return r

if __name__ == '__main__':
	map = load_input(TEST2)
	map = load_input(TEST)
	map = load_input(load_file())
	first = first_part(map)
	print(f'First part: {first}')
	second = second_part(map)
	print(f'Second part: {second}')
