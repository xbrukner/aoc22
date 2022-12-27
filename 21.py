from typing import Optional, Union
from dataclasses import dataclass, field
import operator

task = '21'
TEST = """root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32""".split('\n')


Operation = Union[int, tuple[str, str, str]]
Input = dict[str, Operation]


def load_file() -> list[str]:
	lines = []
	with open(f'{task}.in') as file:
		while line := file.readline().rstrip():
			lines.append(line)
	return lines


def load_input(lines: list[str]) -> Input:
	res = {}
	for line in lines:
		name, operation = line.split(':')
		if operation.lstrip().isnumeric():
			res[name] = int(operation.lstrip())
		else:
			first, op, second = operation.lstrip().split(' ')
			res[name] = first, op, second
	return res


@dataclass
class Tree:
	input: Input
	to_process: list[str] = field(default_factory=list)
	missing: dict[str, set[str]] = field(default_factory=dict)
	resolved: dict[str, int] = field(default_factory=dict)

	def __post_init__(self):
		self.to_process = list(self.input.keys())

	def calculate(self, first: str, op: str, second: str) -> int:
		return {
			'+': operator.add,
			'-': operator.sub,
			'*': operator.mul,
			'/': operator.floordiv,
			'=': lambda x, y: int(x == y)
		}[op](self.resolved[first], self.resolved[second])

	def add_item(self, item: str, value: int):
		self.resolved[item] = value
		if item in self.missing:
			self.to_process.extend(self.missing[item])
			del self.missing[item]

	def add_dependency(self, item: str, on: str):
		if on not in self.missing:
			self.missing[on] = set()
		self.missing[on].add(item)

	def solve(self):
		while self.to_process:
			item = self.to_process.pop()
			if isinstance(self.input[item], int):
				self.add_item(item, self.input[item])
			else:
				first, op, second = self.input[item]
				if first in self.resolved and second in self.resolved:
					self.add_item(item, self.calculate(first, op, second))
				else:
					if first not in self.resolved:
						self.add_dependency(item, first)
					if second not in self.resolved:
						self.add_dependency(item, second)

	def propagate(self, item: str, target: Optional[int] = None):
		if item not in self.input:
			self.resolved[item] = target
			return
		first, op, second = self.input[item]
		missing = first if first not in self.resolved else second
		index = 0 if missing == first else 1
		other = self.resolved[first] if first in self.resolved else self.resolved[second]
		# print(f'{target} = {missing if index == 0 else other} {op} {missing if index == 1 else other}')
		result = {
			'=': [lambda: other] * 2,
			'/': [lambda: target * other, lambda: other // target],
			'-': [lambda: target + other, lambda: other - target],
			'+': [lambda: target - other] * 2,
			'*': [lambda: target // other] * 2,
		}[op][index]()
		# print(missing, result)
		self.propagate(missing, result)


def first_part(input: Input) -> int:
	tree = Tree(input)
	tree.solve()
	return tree.resolved['root']


def second_part(input: Input) -> int:
	del input['humn']
	input['root'] = input['root'][0], '=', input['root'][2]
	tree = Tree(input)
	tree.solve()
	tree.propagate('root')
	return tree.resolved['humn']


if __name__ == '__main__':
	input = load_input(TEST)
	input = load_input(load_file())
	first = first_part(input)
	print(f'First part: {first}')
	second = second_part(input)
	print(f'Second part: {second}')

