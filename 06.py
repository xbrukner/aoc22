task = '06'
Input = list[str]
Occurences = dict[str, int]


def load_input() -> Input:
	with open(f"{task}.in") as file:
		return file.readline().rstrip()


def add_occurence(occurences: Occurences, letter: str) -> None:
	if letter in occurences:
		occurences[letter] += 1
	else:
		occurences[letter] = 1


def remove_occurence(occurences: Occurences, letter: str) -> None:
	if occurences[letter] == 1:
		del occurences[letter]
	else:
		occurences[letter] -= 1


def find_distinct_sequence(input: Input, size: int) -> int:
	received: Occurences = {}
	for letter in input[:size]:
		add_occurence(received, letter)

	for i in range(size, len(input)):
		if len(received) == size:
			return i
		remove_occurence(received, input[i - size])
		add_occurence(received, input[i])


def first_part(input: Input) -> int:
	return find_distinct_sequence(input, 4)


def second_part(input: Input) -> int:
	return find_distinct_sequence(input, 14)


if __name__ == '__main__':
	input = load_input()
	first = first_part(input)
	print(f"First task: {first}")
	second = second_part(input)
	print(f"Second task: {second}")
