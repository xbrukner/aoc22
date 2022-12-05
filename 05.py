import copy

task = '05'
test_input = """    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2"""

Lines = list[str]
Split_input = tuple[Lines, Lines]
Stacks = list[list[str]]
Movement = tuple[int, int, int]
Movements = list[Movement]
Input = tuple[Stacks, Movements]


def load_task() -> Input:
	lines = []
	with open(f"{task}.in") as file:
		while line := file.readline():
			lines.append(line.rstrip())
	stacks, movements = split_input(lines)
	return parse_stacks(stacks), parse_movements(movements)


def split_input(input: Lines) -> Split_input:
	split = input.index("")
	return input[0:split], input[split + 1:]



def parse_stacks(lines: Lines) -> Stacks:
	parsed = [
		[
			line[index] if 'A' <= line[index] <= 'Z' else None
			for index in range(1, len(line), 4)
		]
		for line in lines[:-1]
	]

	return [
		[
			parsed[y][x] for y in reversed(range(len(parsed))) if parsed[y][x]
		]
		for x in range(len(parsed[0]))
	]


def parse_movement(line: str) -> Movement:
	split = line.split(' ')
	return int(split[1]), int(split[3]), int(split[5])


def parse_movements(lines: Lines) -> Movements:
	return [parse_movement(line) for line in lines]


def move_first(stacks: Stacks, movement: Movement) -> None:
	count, frm, to = movement
	for _ in range(count):
		stacks[to - 1].append(stacks[frm - 1].pop())


def first_part(input: Input) -> str:
	original_stacks, movements = input
	stacks = copy.deepcopy(original_stacks)
	for movement in movements:
		move_first(stacks, movement)
	return ''.join([stack[-1] for stack in stacks])


def move_second(stacks: Stacks, movement: Movement) -> None:
	count, frm, to = movement
	stacks[to - 1].extend(stacks[frm - 1][-count:])
	del stacks[frm - 1][-count:]


def second_part(input: Input) -> str:
	original_stacks, movements = input
	stacks = copy.deepcopy(original_stacks)
	for movement in movements:
		move_second(stacks, movement)
	return ''.join([stack[-1] for stack in stacks])


if __name__ == '__main__':
	input = load_task()
	#stacks, movements = split_input(test_input.split('\n'))
	#input = parse_stacks(stacks), parse_movements(movements)
	first = first_part(input)
	print(f"First part: {first}")
	second = second_part(input)
	print(f"Second part: {second}")
