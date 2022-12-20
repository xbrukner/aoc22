from dataclasses import dataclass, field
from typing import Optional
from time import ctime
from functools import reduce

task='19'
TEST="""Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian. 
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.""".split('\n')


@dataclass
class Blueprint:
	index: int
	ore: int
	clay: int
	obsidian: tuple[int, int] # ore, clay
	geode: tuple[int, int] # clay, obsidian


@dataclass
class State:
	mined: list[int, int, int, int] = field(default_factory=lambda: [0, 0, 0, 0])
	robots: list[int, int, int, int] = field(default_factory=lambda: [1, 0, 0, 0])
	build_now: Optional[int] = field(default=None)
	minutes: int = field(default=0)

	def move_time(self, by: int) -> 'State':
		robots = [self.robots[i] - 1 if self.build_now == i else self.robots[i] for i in range(4)]
		mined = [
			self.mined[i] + robots[i] * by for i in range(4)
		]
		robots = self.robots.copy()

		return State(
			mined=mined,
			robots=robots,
			minutes=self.minutes + by
		)

	def what_to_build(self, blueprint: Blueprint) -> list[int]:
		res = []
		if self.mined[0] >= blueprint.ore:
			res.append(0)
		if self.mined[0] >= blueprint.clay:
			res.append(1)
		if self.mined[0] >= blueprint.obsidian[0] and self.mined[1] >= blueprint.obsidian[1]:
			res.append(2)
		if self.mined[0] >= blueprint.geode[0] and self.mined[2] >= blueprint.geode[1]:
			res.append(3)
		return res

	def build(self, what: int, blueprint: Blueprint) -> 'State':
		mined = self.mined.copy()
		robots = self.robots.copy()

		if what == 0:
			mined[0] -= blueprint.ore
		elif what == 1:
			mined[0] -= blueprint.clay
		elif what == 2:
			mined[0] -= blueprint.obsidian[0]
			mined[1] -= blueprint.obsidian[1]
		elif what == 3:
			mined[0] -= blueprint.geode[0]
			mined[2] -= blueprint.geode[1]
		else:
			raise
		robots[what] += 1

		return State(
			mined=mined,
			robots=robots,
			build_now=what,
			minutes=self.minutes
		)


def parse_line(line: str) -> Blueprint:
	sentences = [s.split(' ') for s in line.split('.')]
	index = int(sentences[0][1].split(':')[0])
	ore = int(sentences[0][-2])
	clay = int(sentences[1][-2])
	obsidian = int(sentences[2][-5]), int(sentences[2][-2])
	geode = int(sentences[3][-5]), int(sentences[3][-2])
	return Blueprint(index, ore, clay, obsidian, geode)


def parse(lines: list[str]) -> list[Blueprint]:
	return [parse_line(line) for line in lines]


def load_lines() -> list[str]:
	lines = []
	with open(f'{task}.in') as file:
		while line := file.readline().rstrip():
			lines.append(line)
	return lines


def naive_search(blueprint: Blueprint, index: int) -> int:
	minutes = 20
	states = [State()]
	for minute in range(minutes):
		new_states = []
		for state in states:
			new_states.append(state.move_time(1))
			for option in state.what_to_build(blueprint):
				new_states.append(state.build(option, blueprint).move_time(1))
		states = new_states
		print(f'Index: {index}, minute: {minute + 1}, len: {len(states)}')
	return max([state.mined[3] for state in states]) * index


def build_next(max_minutes: int, what: int, blueprint: Blueprint, states: list[State]) -> Optional[State]:
	for minute in range(max_minutes):
		new_states = []
		for state in states:
			if state.minutes == max_minutes:
				continue
			if what in state.what_to_build(blueprint):
				return state.build(what, blueprint).move_time(1)
			new_states.append(state.move_time(1))
		states = new_states
	return None


def smarter_search(max_minutes: int, blueprint: Blueprint) -> int:
	print(f"Smarter search: {blueprint.index}")
	states: dict[tuple[int, int, int, int], dict[tuple[int, int, int], State]] = {(1, 0, 0, 0): {(0, 0, 0): State()}}
	current_max = -1
	matched = True
	iteration = 0
	while matched:
		print(f" iteration {iteration}, time {ctime()}")
		iteration += 1
		matched = False
		current_max = max(current_max, max([s.move_time(max_minutes - s.minutes).mined[3] for state in states.values() for s in state.values()]))
		new_states = {}
		for possible_states in states.values():
			for state in possible_states.values():
				for what in range(4):
					if success := build_next(max_minutes, what, blueprint, [state]):
						key: tuple[int, int, int, int] = tuple(success.robots)
						dict_key: tuple[int, int, int] = success.mined[3], success.mined[2], success.mined[1]
						if key not in new_states or dict_key not in new_states[key] or new_states[key][dict_key].minutes > success.minutes:
							if key not in new_states:
								new_states[key] = {}
							new_states[key][dict_key] = success
							matched = True
		states = new_states
	# [(key, dict_key, s) for key, state in states.items() for dict_key, s in state.items() if s.move_time(max_minutes - s.minutes).mined[3] == 10]
	return current_max * blueprint.index


def first_part(input: list[Blueprint]) -> int:
	return sum([smarter_search(24, blueprint) for blueprint in input])


def second_part(input: list[Blueprint]) -> int:
	return reduce(lambda x, y: x * y, [int(smarter_search(32, blueprint) / blueprint.index) for blueprint in input[:3]])


# ore -> clay
# ore + clay -> obsidian
# ore + obsidian -> geode
# 4; 2; 3, 14; 2, 7
# 1 obsidian = 14 clay, 3 ore
# 1 geode = 7 obsidian, 2 ore
# for 1 geode in 1 step? in 2 step?
# what is the limiting factor?
# Can I calculate maximum?
# If I don't build anything, what will I have in 24? -> score
# 1000 combinations - up to 10 of each kind. Next to build from current fastest options.


if __name__ == '__main__':
	input = parse(TEST)
	input = parse(load_lines())
	#first = first_part(input)
	#print(f'First part: {first}')
	second = second_part(input)
	print(f'Second part: {second}')