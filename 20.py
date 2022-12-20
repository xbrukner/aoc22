from dataclasses import dataclass, field

task = '20'
TEST="""1
2
-3
3
-2
0
4""".split('\n')
TEST="""1
2
-3
3
-2
0
4""".split('\n')


def load_file() -> list[int]:
	lines = []
	with open(f"{task}.in") as file:
		while line := file.readline().rstrip():
			lines.append(int(line))
	return lines


def load_input(lines: list[str]) -> list[int]:
	return [int(line) for line in lines]


@dataclass
class Item:
	number: int
	prev: 'Item'
	next: 'Item'

	def move(self, relative: int):
		if relative == 0:
			return
		# pop current
		self.prev.next = self.next
		self.next.prev = self.prev
		if relative > 0:
			after = self.next
			for i in range(relative - 1):
				after = after.next
			self.prev = after
			self.next = after.next
			after.next.prev = self
			after.next = self
		else:
			before = self.prev
			for i in range(-relative - 1):
				before = before.prev
			self.next = before
			self.prev = before.prev
			before.prev.next = self
			before.prev = self


@dataclass
class LinkedList:
	items: list[Item] = field(default_factory=list)

	def append(self, number: int):
		if not self.items:
			item = Item(number, None, None)
			item.prev = item
			item.next = item
		else:
			item = Item(number, self.items[-1], self.items[0])
			self.items[-1].next = item
			self.items[0].prev = item
		self.items.append(item)

	def print(self):
		item = self.items[0]
		while item.next != self.items[0]:
			print(f'{item.number} ', end='')
			item = item.next
		print(f'{item.number}')
		return


def build_list(input: list[int]) -> LinkedList:
	ll = LinkedList()
	for number in input:
		ll.append(number)
	return ll


def rotate(ll: LinkedList) -> Item:
	zero = None
	for item in ll.items:
		move = item.number % (len(ll.items) - 1) if item.number >= 0 else item.number % -(len(ll.items) - 1)
		if item.number == 0:
			zero = item
		item.move(move)
	return zero


def result(ll: LinkedList, zero: Item) -> int:
	moves: set[int] = {num % (len(ll.items)) for num in [1000, 2000, 3000]}
	results: dict[int, int] = {}
	for i in range(max(moves) + 1):
		if i in moves:
			results[i] = zero.number
		zero = zero.next
	return sum(results.values())


def first_part(input: list[int]) -> int:
	ll = build_list(input)
	zero = rotate(ll)
	return result(ll, zero)


def second_part(input: list[int]) -> int:
	ll = build_list([num * 811589153 for num in input])
	for i in range(10):
		zero = rotate(ll)
	return result(ll, zero)


if __name__ == '__main__':
	numbers = load_input(TEST)
	numbers = load_file()
	first = first_part(numbers)
	print(f'First part {first}')
	second = second_part(numbers)
	print(f'Second part {second}')
