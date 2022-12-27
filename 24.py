from dataclasses import dataclass

task = '24'
TEST = """#.#####
#.....#
#>....#
#.....#
#...v.#
#.....#
#####.#""".split('\n')
TEST2 = """#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#""".split('\n')

Direction = tuple[int, int]
Position = tuple[int, int]
Directions: dict[str, Direction] = {'^': (0, -1), 'v': (0, 1), '>': (1, 0), '<': (-1, 0)}
All_directions = list(Directions.values()) + [(0, 0)]
Blizzards = dict[Position, list[str]]


def move(pos: Position, dir: Direction) -> Position:
	return pos[0] + dir[0], pos[1] + dir[1]


def load_file() -> list[str]:
	lines = []
	with open(f'{task}.in') as file:
		while line := file.readline().rstrip():
			lines.append(line)
	return lines


@dataclass
class Map:
	start: int
	end: int
	x_size: int
	y_size: int
	blizzards: Blizzards

	def within_bounds(self, pos: Position) -> bool:
		return 0 < pos[0] < self.x_size and 0 < pos[1] < self.y_size

	def move_around(self, pos: Position) -> Position:
		if pos[0] == 0:
			return self.x_size - 1, pos[1]
		if pos[0] == self.x_size:
			return 1, pos[1]
		if pos[1] == 0:
			return pos[0], self.y_size - 1
		if pos[1] == self.y_size:
			return pos[0], 1

	def move_blizzards(self) -> 'Map':
		blizzards = {}
		for pos, dirs in self.blizzards.items():
			for dir in dirs:
				new = move(pos, Directions[dir])
				if not self.within_bounds(new):
					new = self.move_around(new)
				if new not in blizzards:
					blizzards[new] = []
				blizzards[new].append(dir)
		return Map(start=self.start, end=self.end, x_size=self.x_size, y_size=self.y_size, blizzards=blizzards)


def load_map(input: list[str]) -> Map:
	start = input[0].index('.')
	end = input[-1].index('.')
	x_size = len(input[0]) - 1
	y_size = len(input) - 1
	blizzards = {
		(x, y): input[y][x]
		for x in range(1, x_size)
		for y in range(1, y_size)
		if input[y][x] != '.'
	}
	return Map(start=start, end=end, x_size=x_size, y_size=y_size, blizzards=blizzards)


def move_across(start: Position, finish: Position, map: Map) -> tuple[int, Map]:
	steps = 0
	positions: set[Position] = {start}
	while not any(pos == finish for pos in positions):
		map = map.move_blizzards()
		blizzards = map.blizzards.keys()
		positions = set(
			filter(
				lambda moved: moved == finish or moved == start or (map.within_bounds(moved) and moved not in blizzards),
				[
					move(pos, dir)
					for pos in positions
					for dir in All_directions
				]
			)
		)
		steps += 1
	return steps, map


def first_part(map: Map) -> int:
	return move_across((map.start, 0), (map.end, map.y_size), map)[0]


def second_part(map: Map) -> int:
	start = (map.start, 0)
	end = (map.end, map.y_size)
	there = move_across(start, end, map)
	back = move_across(end, start, there[1])
	there_again = move_across(start, end, back[1])
	return there[0] + back[0] + there_again[0]


if __name__ == '__main__':
	map = load_map(TEST)
	map = load_map(TEST2)
	map = load_map(load_file())
	first = first_part(map)
	print(f'First part: {first}')
	second = second_part(map)
	print(f'Second part: {second}')
