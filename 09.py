Position = tuple[int, int]
Rope = tuple[Position, Position]
Instruction = tuple[str, int]
Directions: dict[str, Position] = {
	'R': (1, 0),
	'U': (0, 1),
	'L': (-1, 0),
	'D': (0, -1)
}
TEST = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2""".split("\n")
task = '09'


def parse_instruction(line: str) -> Instruction:
	direction, steps = line.split(' ')
	return direction, int(steps)


def load_instructions() -> list[Instruction]:
	instructions: list[Instruction] = []
	with open(f"{task}.in") as file:
		while line := file.readline().rstrip():
			instructions.append(parse_instruction(line))
	return instructions


def move_position(pos1: Position, pos2: Position) -> Position:
	return pos1[0] + pos2[0], pos1[1] + pos2[1]


def adjacent(pos1: Position, pos2: Position) -> bool:
	return abs(pos1[0] - pos2[0]) <= 1 and abs(pos1[1] - pos2[1]) <= 1


def move_one(rope: Rope, direction: str) -> Rope:
	tail, head = rope
	movement = Directions[direction]
	moved_head = move_position(head, movement)
	if not adjacent(tail, moved_head):
		return head, moved_head
	else:
		return tail, moved_head


def move_tail(head: Position, tail: Position) -> Position:
	if adjacent(head, tail):
		return tail
	x_movement = head[0] - tail[0]
	y_movement = head[1] - tail[1]
	if abs(x_movement) == 2 and abs(y_movement) == 2:
		return head[0] - int(x_movement / 2), head[1] - int(y_movement / 2)
	elif abs(x_movement) == 2:
		return head[0] - int(x_movement / 2), head[1]
	return head[0], head[1] - int(y_movement / 2)


def first_part(instructions: list[Instruction]) -> int:
	rope: Rope = ((0, 0), (0, 0))
	visited: set[Position] = {rope[0]}
	for instruction in instructions:
		for _ in range(instruction[1]):
			rope = move_one(rope, instruction[0])
			visited.add(rope[0])
	return len(visited)


def print_rope(rope: list[Position]):
	for y in range(6):
		for x in range(6):
			index = (x, 5 - y)
			if index not in rope:
				print(".", end='')
			else:
				first = rope.index(index)
				print("H" if first == 0 else first, end='')
		print('\n', end='')
	print('\n', end='')


def second_part(instructions: list[Instruction]) -> int:
	size = 10
	rope: list[Position] = [(0, 0)] * size
	visited: set[Position] = {rope[-1]}
	for instruction in instructions:
		for _ in range(instruction[1]):
			moved_rope = [move_position(rope[0], Directions[instruction[0]])]
			for i in range(1, size):
				moved_rope.append(move_tail(moved_rope[-1], rope[i]))
			rope = moved_rope
			visited.add(rope[-1])
	return len(visited)


if __name__ == '__main__':
	TEST_INSTRUCTIONS = [parse_instruction(line) for line in TEST]
	instructions = load_instructions()
	first = first_part(instructions)
	print(f"First part: {first}")
	second = second_part(instructions)
	print(f"Second part: {second}")
