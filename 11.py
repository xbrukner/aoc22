from __future__ import annotations

from dataclasses import dataclass
from copy import deepcopy

task='11'
TEST="""Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1""".split("\n")


def load_input() -> list[str]:
	lines = []
	with open(f"{task}.in", "r") as file:
		while line := file.readline():
			lines.append(line.rstrip())
	return lines


@dataclass
class Number:
	mods: list[int]
	rems: list[int]

	@classmethod
	def from_monkeys(cls, monkeys: List[Monkey], item: int):
		mods = [monkey.test for monkey in monkeys]
		rems = [item % mod for mod in mods]
		return cls(mods=mods, rems=rems)

	def __add__(self, other: int | Number) -> Number:
		if isinstance(other, int):
			rems = [(self.rems[i] + other) % self.mods[i] for i in range(len(self.mods))]
		else:
			rems = [(self.rems[i] + other.rems[i]) % self.mods[i] for i in range(len(self.mods))]
		return Number(mods=self.mods, rems=rems)

	def __mul__(self, other: int) -> Number:
		if isinstance(other, int):
			rems = [(self.rems[i] * other) % self.mods[i] for i in range(len(self.mods))]
		else:
			rems = [(self.rems[i] * other.rems[i]) % self.mods[i] for i in range(len(self.mods))]
		return Number(mods=self.mods, rems=rems)

	def __mod__(self, other: int) -> int:
		return self.rems[self.mods.index(other)]


@dataclass
class Monkey:
	items: list[int | Number]
	operation: str
	test: int
	truth: int
	false: int

	def convert_items(self, monkeys: list[Monkey]):
		self.items = [Number.from_monkeys(monkeys, item) for item in self.items]

	def move_items(self, divide: bool) -> list[tuple[int, int | Number]]:
		moves = [self.process_item(item, divide) for item in self.items]
		self.items = []
		return moves

	def process_item(self, item: int | Number, divide: bool) -> tuple[int, int | Number]:
		inspected = self.calculate(item)
		bored = int(inspected / 3) if divide else inspected
		if bored % self.test == 0:
			return self.truth, bored
		else:
			return self.false, bored

	def calculate(self, item: int | Number) -> int | Number:
		if self.operation == 'old * old':
			return item * item
		elif self.operation == 'old + old':
			return item + item
		elif self.operation.startswith('old * '):
			return item * int(self.operation[5:])
		elif self.operation.startswith('old + '):
			return item + int(self.operation[5:])
		raise f"Unknown operation {self.operation}"


def parse_monkey(lines: list[str]) -> Monkey:
	items = [int(item) for item in lines[1].split(':')[1].split(',')]
	operation = lines[2].split('=')[1].strip()
	test = int(lines[3].split('by')[1].strip())
	truth = int(lines[4].split(' ')[-1])
	false = int(lines[5].split(' ')[-1])
	return Monkey(items=items, operation=operation, test=test, truth=truth, false=false)


def parse_monkeys(lines: list[str]) -> list[Monkey]:
	return [parse_monkey(lines[x:x+7]) for x in range(0, len(lines), 7)]


def first_part(monkeys: list[Monkey]) -> int:
	inspected = [0] * len(monkeys)
	for turn in range(20):
		for i in range(len(monkeys)):
			move = monkeys[i].move_items(True)
			inspected[i] += len(move)
			for index, item in move:
				monkeys[index].items.append(item)
	inspected.sort()
	return inspected[-2] * inspected[-1]


def second_part(monkeys: list[Monkey]) -> int:
	for monkey in monkeys:
		monkey.convert_items(monkeys)
	inspected = [0] * len(monkeys)
	for turn in range(10000):
		for i in range(len(monkeys)):
			move = monkeys[i].move_items(False)
			inspected[i] += len(move)
			for index, item in move:
				monkeys[index].items.append(item)
	inspected.sort()
	return inspected[-2] * inspected[-1]


if __name__ == '__main__':
	monkeys = parse_monkeys(load_input())
	first = first_part([deepcopy(monkey) for monkey in monkeys])
	print(f"First part {first}")
	second = second_part([deepcopy(monkey) for monkey in monkeys])
	print(f"Second part {second}")


