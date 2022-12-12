from dataclasses import dataclass, field
from queue import PriorityQueue, Empty
from typing import Optional

task = '12'
TEST="""Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi""".split("\n")
Lines = list[str]
Position = tuple[int, int]
Map = tuple[Lines, Position, Position]
Steps = list[list[int]]


def load_map() -> Map:
	lines = []
	with open(f"{task}.in") as file:
		while line := file.readline().rstrip():
			lines.append(line)
	return extract_start_stop(lines)


def extract_start_stop(lines: Lines) -> Map:
	start: Optional[Position] = None
	end: Optional[Position] = None
	newlines: Lines = []
	for y, line in enumerate(lines):
		newline = str(line)
		if 'S' in line:
			index = line.index('S')
			start = (index, y)
			newline = newline[:index] + 'a' + newline[index + 1:]
		if 'E' in line:
			index = line.index('E')
			end = (index, y)
			newline = newline[:index] + 'z' + newline[index + 1:]
		newlines.append(newline)
	if start is None or end is None:
		raise "Invalid input"
	return newlines, start, end


def moves(pos: Position) -> list[Position]:
	return [
		(pos[0] - 1, pos[1]),
		(pos[0] + 1, pos[1]),
		(pos[0], pos[1] - 1),
		(pos[0], pos[1] + 1),
	]


def filter_move(start: Position, move: Position, lines: Lines) -> bool:
	return 0 <= move[0] < len(lines[0]) and \
		0 <= move[1] < len(lines) and \
		ord(lines[move[1]][move[0]]) - ord(lines[start[1]][start[0]]) <= 1


@dataclass(order=True)
class PrioritizedItem:
	priority: int
	item: Position = field(compare=False)


def dijkstra(map: Map) -> Optional[int]:
	lines, start, end = map
	steps: Steps = [[0] * len(lines[1]) for x in range(len(lines))]
	visited: Steps = [[False] * len(lines[1]) for x in range(len(lines))]
	queue = PriorityQueue()
	queue.put(PrioritizedItem(0, start))

	try:
		while item := queue.get_nowait():
			step: int = item.priority
			pos: Position = item.item
			if visited[pos[1]][pos[0]]:
				continue
			steps[pos[1]][pos[0]] = step
			visited[pos[1]][pos[0]] = True
			next_moves = filter(lambda next_move: filter_move(pos, next_move, lines), moves(pos))
			for move in next_moves:
				if not visited[move[1]][move[0]]:
					queue.put(PrioritizedItem(step + 1, move))
	except Empty:
		if visited[end[1]][end[0]]:
			return steps[end[1]][end[0]]


def first_half(map: Map) -> int:
	return dijkstra(map)


def second_half(map: Map) -> int:
	lines, _, end = map
	starts = [
		(x, y)
		for y, line in enumerate(lines)
		for x in range(len(line))
		if line[x] == 'a'
	]
	return min(filter(None, [
		first_half((lines, start, end)) for start in starts
	]))


if __name__ == '__main__':
	map = extract_start_stop(TEST)
	map = load_map()
	first = first_half(map)
	print(f"First half: {first}")
	second = second_half(map)
	print(f"Second half: {second}")
