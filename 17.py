from dataclasses import dataclass, field
from typing import Iterator
task = '17'
TEST=""">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"""
rocks = [
	[(0, 0), (1, 0), (2, 0), (3, 0)], #-
	[(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)], #+
	[(2, 0), (2, 1), (2, 2), (1, 0), (0, 0)], #inversed L
	[(0, 0), (0, 1), (0, 2), (0, 3)], #|
	[(0, 0), (1, 0), (0, 1), (1, 1)] #o
]
heights = [1, 3, 3, 4, 2]
Position = tuple[int, int]
Map = set[tuple[int, int]]


def load_input() -> str:
	with open(f'{task}.in') as file:
		return file.readline().rstrip()


def intersects(position: Position, map: Map) -> bool:
	if not 0 <= position[0] < 7:
		return True
	if position[1] < 0:
		return True
	return position in map


def move(position: Position, x: int, y: int) -> Position:
	return position[0] + x, position[1] + y


@dataclass
class Jet:
	movements: str
	iteration: int = 0
	index: int = 0

	def __iter__(self):
		while True:
			for self.index, m in enumerate(self.movements):
				yield m
			self.iteration += 1


def place(movements: Iterator[str], index: int, map: Map) -> list[Position]:
	max_y = max([coord[1] for coord in map], default=-1) + 4
	rock = [move(r, 2, max_y) for r in rocks[index]]
	for movement in movements:
		possibly_moved = [move(pos, 1 if movement == '>' else -1, 0) for pos in rock]
		if not any([intersects(pos, map) for pos in possibly_moved]):
			rock = possibly_moved
		move_down = [move(pos, 0, -1) for pos in rock]
		if not any([intersects(pos, map) for pos in move_down]):
			rock = move_down
		else:
			return rock


def first_part(directions: str) -> int:
	movements = iter(Jet(directions))
	map: Map = set()
	for index in range(2022):
		rock = place(movements, index % 5, map)
		for pos in rock:
			map.add(pos)
	return max([coord[1] for coord in map]) + 1


@dataclass
class Stats:
	max: list[int] = field(default_factory=list)
	stone: list[int] = field(default_factory=list)
	index: list[int] = field(default_factory=list)

	def add(self, map: Map, index: int):
		self.max.append(max([coord[1] for coord in map]) + 1)
		self.stone.append(index % 5)
		self.index.append(index)

	def matches(self):
		return len(self.max) > 2 and\
			all([stone == self.stone[1] for stone in self.stone[1:]]) and\
			all([self.max[2] - self.max[1] == self.max[i] - self.max[i - 1] for i in range(2, len(self.max))])


def second_part(directions: str) -> int:
	jet = Jet(directions)
	movements = iter(jet)
	stats: dict[int, Stats] = dict()
	map: Map = set()
	index = 0
	while jet.iteration != 15:
		curr = jet.iteration
		rock = place(movements, index % 5, map)
		for pos in rock:
			map.add(pos)
		index += 1 # Number of rocks that fell
		if jet.index not in stats:
			stats[jet.index] = Stats()
		stats[jet.index].add(map, index)
		if curr != jet.iteration:
			print(jet.iteration)
	matching = { index: s for index, s in stats.items() if s.matches() }
	reference: Stats = next(iter(matching.values()))

	period = reference.index[2] - reference.index[1]
	diff = reference.max[2] - reference.max[1]
	before = reference.index[1]
	multiplier, rest = divmod(1_000_000_000_000, period)
	while rest < before: # Too lazy to math
		multiplier -= 1
		rest += period
	repeated = multiplier * diff
	start_end = next(iter(([
		s.max[s.index.index(rest)] for s in stats.values()
		if rest in s.index
	])))
	return repeated + start_end


if __name__ == '__main__':
	input = TEST
	#input = load_input()
	first = first_part(input)
	print(f"First part: {first}")
	second = second_part(input)
	print(f"Second part: {second}")
