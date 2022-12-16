from dataclasses import dataclass
from typing import Optional
from functools import cached_property

task = '15'
TEST = """Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3""".split("\n")

Position = tuple[int, int] # x, y


@dataclass
class Interval:
	left: int
	right: int

	def __cmp__(self, other: 'Interval'):
		return other.right - self.right if self.left == other.left else other.left - self.left

	def intersects(self, other: 'Interval') -> bool:
		return self.left <= other.left <= self.right or other.left <= self.left <= other.right

	def join(self, other: 'Interval') -> 'Interval':
		if not self.intersects(other):
			raise 'Cannot join disjoint intervals'
		return Interval(left=min(self.left, other.left), right=max(self.right, other.right))

	def __len__(self):
		return self.right - self.left + 1


class Intervals:
	intervals: list[Interval]

	def __init__(self, intervals: list[Interval]):
		self.intervals = []
		for interval in intervals:
			self.add(interval)

	def add(self, interval: Interval):
		# This can be improved possibly to nlog n insert, but not for now
		for index in range(len(self.intervals)):
			if self.intervals[index].intersects(interval):
				# In case of intersect, extract it, join it, and recursively add
				new = self.intervals.pop(index).join(interval)
				self.add(new)
				return
		# No matches -> add new and sort
		self.intervals.append(interval)

	def in_between(self) -> list[int]:
		# Assumption - the missing beacon is next to interval
		indices: list[int] = []
		for interval in self.intervals:
			indices.append(interval.left - 1)
			indices.append(interval.right + 1)
		return indices

	def __len__(self) -> int:
		return sum([len(interval) for interval in self.intervals])


@dataclass
class SBPair:
	sensor: Position
	beacon: Position

	@cached_property
	def distance(self):
		return abs(self.sensor[0] - self.beacon[0]) +\
			abs(self.sensor[1] - self.beacon[1])

	def intersects_line(self, line) -> Optional[Interval]:
		# Note: Beacon is NOT included - there can be no overlap
		if self.sensor[1] - self.distance <= line <= self.sensor[1] + self.distance:
			difference = self.distance - abs(self.sensor[1] - line) # number of blocks to each side from the middle
			left = self.sensor[0] - difference
			right = self.sensor[0] + difference
			if self.beacon[1] == line: # Beacon included -> move the line
				if left == self.beacon[0]:
					left += 1
				else:
					right -= 1
			return Interval(left, right)
		return None


def load_input() -> list[str]:
	lines = []
	with open(f"{task}.in") as file:
		while line := file.readline().rstrip():
			lines.append(line)
	return lines


def parse_xy(input: str) -> Position:
	x, y = [int(comma.split('=')[1]) for comma in input.split(',')]
	return x, y


def parse_line(line: str) -> SBPair:
	sensor, beacon = line.split(':')
	return SBPair(sensor=parse_xy(sensor), beacon=parse_xy(beacon))


def parse_input(lines: list[str]) -> list[SBPair]:
	return [parse_line(line) for line in lines]


def intervals_for_line(input: list[SBPair], line: int) -> Intervals:
	return Intervals(list(filter(None, [sb.intersects_line(line) for sb in input])))


def first_half(input: list[SBPair]) -> int:
	line = 2000000
	return len(intervals_for_line(input, line))


def second_half(input: list[SBPair]) -> int:
	lines = 4000000 # Assumption - it is not on the edge
	beacons: set[Position] = { sb.beacon for sb in input }
	for line in range(lines + 1):
		for x in intervals_for_line(input, line).in_between():
			if x < 0 or x > lines:
				continue
			if (x, line) not in beacons:
				print(x, line)
				return x * lines + line


if __name__ == '__main__':
	input = parse_input(TEST)
	input = parse_input(load_input())
	first = first_half(input)
	print(f'First half {first}')
	second = second_half(input)
	print(f'Second half {second}')
