

task = '16'
TEST = """Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II""".split('\n')

Valves = dict[str, int]
Tunnels = dict[str, list[str]]
Input = tuple[Valves, Tunnels]
# releasing, released, opened valves
# for each combination of opened valves,
#  the one with bigger released wins
#  Are opened valves combinations comparable?
#   if one combination is sub another, use the bigger one?
# for now, just join on the possible opened valves - and compare total released gas
State = dict[str, dict[frozenset[str], int]] # location -> possible combinations of opened valves and released gas
State2 = dict[tuple[str, str], dict[frozenset[str], int]] # location -> possible combinations of opened valves and released gas

# Actions: nothing, open current valve, move to another valve
def add_line(line: str, valves: Valves, tunnels: Tunnels):
	name = line.split(' ')[1]
	rate = int(line.split('=')[1].split(';')[0])
	dst = [tunnel.rstrip(',') for tunnel in line.split(' ')[9:]]
	valves[name] = rate
	tunnels[name] = dst


def parse_input(lines: list[str]) -> Input:
	valves: Valves = {}
	tunnels: Tunnels = {}
	for line in lines:
		add_line(line, valves, tunnels)
	return valves, tunnels


def load_input() -> list[str]:
	lines = []
	with open(f"{task}.in") as file:
		while line := file.readline().rstrip():
			lines.append(line)
	return lines


def update_state(state: State, valve: str, valves: frozenset[str], score: int):
	if valve not in state:
		state[valve] = {}
	state[valve][valves] = max(score, state[valve].get(valves, -1))


def update_state2(state: State2, valve1: str, valve2: str, valves: frozenset[str], score: int):
	valve: tuple[str, str] = tuple(sorted([valve1, valve2]))
	if valve not in state:
		state[valve] = {}
	state[valve][valves] = max(score, state[valve].get(valves, -1))


def first_part(input: Input) -> int:
	valves, tunnels = input
	minutes = 30
	state: State = {'AA': {frozenset(): 0}}
	for _ in range(minutes):
		newState: State = {}
		for valve, options in state.items():
			for opened, score in options.items():
				options[opened] += sum([valves[single] for single in list(opened)])
		# actions: nothing, open valve, move
		for valve, options in state.items():
			for opened, score in options.items():
				# Nothing
				update_state(newState, valve, opened, score)
				# Move
				for dst in tunnels[valve]:
					if dst not in opened:
						update_state(newState, dst, opened, score)
				# Open valve
				if valves[valve]:
					update_state(newState, valve, opened | {valve}, score)
		state = newState
	return max([
		score
		for _valve, options in state.items()
		for _valves, score in options.items()
	])


def second_part(input: Input) -> int:
	valves, tunnels = input
	minutes = 26
	state: State2 = {('AA', 'AA'): {frozenset(): 0}}
	nonZero = len([valve for valve, score in valves.items() if score > 0])
	for minute in range(minutes - 1):
		newState: State2 = {}
		# actions: nothing, open valve, move
		for pos, options in state.items():
			for opened, score in options.items():
				first, second = pos
				# Nothing - first
				#  - second nothing
				update_state2(newState, first, second, opened, score)
				if nonZero == len(opened):
					print(f'All opened: {score}')
					continue
				#  - second move
				for dst in tunnels[second]:
					update_state2(newState, first, dst, opened, score)
				#  - second open valve
				if valves[second]:
					update_state2(newState, first, second, opened | {second}, score)

				# Move - first
				for dst in tunnels[first]:
					#  - second nothing
					update_state2(newState, dst, second, opened, score)
					#  - second move
					for dst2 in tunnels[second]:
						update_state2(newState, dst, dst2, opened, score)
					# - second open valve
					if valves[second]:
						update_state2(newState, dst, second, opened | {second}, score)

				# Open valve - first
				if valves[first]:
					# - second nothing
					update_state2(newState, first, second, opened | {first}, score)
					#  - second move
					for dst in tunnels[second]:
						update_state2(newState, first, dst, opened | {first}, score)
					#  - second open valve
					if valves[second]:
						update_state2(newState, first, second, opened | {first, second}, score)
		for pos, options in newState.items():
			for opened, score in options.items():
				options[opened] += sum([valves[single] for single in list(opened)])
		state = newState
		newState: State2 = {}
		for pos, options in state.items():
			for opened, score in options.items():
				if not any([opened.issubset(opened2) and score < score2 for opened2, score2 in options.items()]):
					first, second = pos
					update_state2(newState, first, second, opened, score)
		state = newState
		print(minute)
	return max([
		score
		for _valve, options in state.items()
		for _valves, score in options.items()
	])


if __name__ == '__main__':
	input = parse_input(TEST)
	input = parse_input(load_input())
	first = first_part(input)
	print(f'First part: {first}')
	second = second_part(input)
	print(f'Second part: {second}')
