from dataclasses import dataclass
from typing import Dict

task = '02'


@dataclass(frozen=True, eq=True)
class Result:
	score: int

	def __int__(self) -> int:
		return self.score


WIN = Result(6)
DRAW = Result(3)
LOST = Result(0)


@dataclass(frozen=True, eq=True)
class Shape:
	score: int

	def __int__(self) -> int:
		return self.score


ROCK = Shape(1)
PAPER = Shape(2)
SCISSORS = Shape(3)
CMP_RESULTS: dict[Shape, dict[Shape, Result]] = {
	ROCK: {ROCK: DRAW, PAPER: WIN, SCISSORS: LOST},
	PAPER: {ROCK: LOST, PAPER: DRAW, SCISSORS: WIN},
	SCISSORS: {ROCK: WIN, PAPER: LOST, SCISSORS: DRAW},
}
LETTERS: dict[str, Shape] = {
	'A': ROCK,
	'B': PAPER,
	'C': SCISSORS,
	'X': ROCK,
	'Y': PAPER,
	'Z': SCISSORS,
}

# Part 2
RESULT_LETTERS: dict[str, Result] = {
	'X': LOST,
	'Y': DRAW,
	'Z': WIN,
}
CHOOSE: dict[Shape, dict[Result, Shape]] = {
	opponent: {
		result: shape for (shape, result) in cmp.items()
	}
	for (opponent, cmp) in CMP_RESULTS.items()
}


def choose(opponent: Shape, result: Result) -> Shape:
	return CHOOSE[opponent][result]


def compare(opponent: Shape, me: Shape) -> Result:
	return CMP_RESULTS[opponent][me]


def load_shape(letter: str) -> Shape:
	return LETTERS[letter]


def load_result(letter: str) -> Result:
	return RESULT_LETTERS[letter]


Input = list[tuple[Shape, str]]


def load_input() -> Input:
	input: Input = []
	with open(f"{task}.in") as file:
		while line := file.readline():
			letters = line.rstrip().split(' ')
			input.append((load_shape(letters[0]), letters[1]))
	return input


def first_part(input: Input) -> int:
	return sum([
		int(compare(opponent, me := load_shape(letter))) + int(me)
		for (opponent, letter) in input
	])


def second_part(input: Input) -> int:
	return sum([
		int(me := choose(opponent, result := load_result(letter))) +
		int(result)
		for (opponent, letter) in input
	])


if __name__ == '__main__':
	input_list = load_input()
	first = first_part(input_list)
	print(f"First part result: {first}")
	second = second_part(input_list)
	print(f"Second part result: {second}")
