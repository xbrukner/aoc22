Input = list[list[int]]
task = '08'
TEST_STR = """30373
25512
65332
33549
35390"""
TEST = [
	[int(tree) for tree in line]
	for line in TEST_STR.split("\n")
]


def load_input() -> Input:
	inp: Input = []
	with open(f"{task}.in") as file:
		while line := file.readline().rstrip():
			inp.append([int(tree) for tree in line])
	return inp


def visible(trees: Input, row: int, col: int) -> bool:
	tree = trees[row][col]
	if row == 0 or col == 0:
		return True
	up = all([trees[x][col] < tree for x in range(0, row)])
	down = all([trees[x][col] < tree for x in range(row + 1, len(trees))])
	left = all([trees[row][y] < tree for y in range(0, col)])
	right = all([trees[row][y] < tree for y in range(col + 1, len(trees[0]))])
	return up or down or left or right


def viewing_score(trees: list[bool]) -> int:
	if all(trees):
		return len(trees)
	else:
		return trees.index(False) + 1


def viewing_distance(trees: Input, row: int, col: int) -> int:
	tree = trees[row][col]
	if row == 0 or col == 0 or row == len(trees) - 1 or col == len(trees[0]) - 1:
		return 0
	up = viewing_score(list(reversed([trees[x][col] < tree for x in range(0, row)])))
	down = viewing_score([trees[x][col] < tree for x in range(row + 1, len(trees))])
	left = viewing_score(list(reversed([trees[row][y] < tree for y in range(0, col)])))
	right = viewing_score([trees[row][y] < tree for y in range(col + 1, len(trees[0]))])
	return up * down * left * right


def first_part(trees: Input) -> int:
	return [visible(trees, x, y) for x in range(0, len(trees)) for y in range(0, len(trees[0]))].count(True)


def second_part(trees: Input) -> int:
	return max([viewing_distance(trees, x, y) for x in range(0, len(trees)) for y in range(0, len(trees[0]))])


if __name__ == '__main__':
	inp = load_input()
	first = first_part(inp)
	print(f"{first}")
	second = second_part(inp)
	print(f"{second}")

