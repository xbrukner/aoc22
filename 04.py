task = '04'

Range = tuple[int, int]
Ranges = tuple[Range, Range]
Input = list[Ranges]


def load_range(range: str) -> Range:
	nums = range.split('-')
	return int(nums[0]), int(nums[1])


def load_input():
	input: Input = []
	with open(f"{task}.in") as file:
		while line := file.readline().rstrip():
			ranges = line.split(',')
			input.append((load_range(ranges[0]), load_range(ranges[1])))
	return input


def range_covers(first: Range, second: Range) -> bool:
	return first[0] <= second[0] and first[1] >= second[1]


def covers(ranges: Ranges) -> bool:
	first, second = ranges
	return range_covers(first, second) or range_covers(second, first)


def first_part(input: Input) -> int:
	return len([ranges for ranges in input if covers(ranges)])


def range_overlaps(first: Range, second: Range) -> bool:
	return first[0] <= second[0] <= first[1]


def overlaps(ranges: Ranges) -> bool:
	first, second = ranges
	return range_overlaps(first, second) or range_overlaps(second, first)


def second_part(input: Input) -> int:
	return len([ranges for ranges in input if overlaps(ranges)])


if __name__ == '__main__':
	input = load_input()
	first = first_part(input)
	print(f"First part: {first}")
	second = second_part(input)
	print(f"Second part: {second}")
