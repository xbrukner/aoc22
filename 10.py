from typing import Optional

task = '10'

TEST = """noop
addx 3
addx -5""".split("\n")

State = tuple[int, Optional[int]]


def load_program() -> list[str]:
	lines = []
	with open(f"{task}.in") as file:
		while line := file.readline().rstrip():
			lines.append(line)
	return lines


def compute(state: State, lines: list[str]) -> State:
	if state[1]:
		return state[0] + state[1], None
	else:
		line = lines.pop(0)
		if line == 'noop':
			return state
		return state[0], int(line[4:])


def first_part(lines: list[str]) -> int:
	lines = lines.copy()
	state = (1, None)
	result = 0
	positions = [20, 60, 100, 140, 180, 220]
	for x in range(1, 230):
		if x in positions:
			print(F"{x} {state[0]} {len(lines)} = {x * state[0]}")
			result += state[0] * x
		state = compute(state, lines)
	return result


def second_part(lines: list[str]):
	lines = lines.copy()
	state = (1, None)
	for y in range(6):
		for x in range(40):
			if state[0] - 1 <= x <= state[0] + 1:
				print('#', end='')
			else:
				print('.', end='')
			state = compute(state, lines)
		print('\n', end='')


if __name__ == '__main__':
	program = load_program()
	first = first_part(program)
	print(f"First part: {first}")
	second_part(program)

