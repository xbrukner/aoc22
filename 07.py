from dataclasses import dataclass, field
from typing import Optional
TASK = '07'
Input = list[str]
TEST: Input = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k""".split("\n")


def load_input() -> Input:
	lines = []
	with open(f"{TASK}.in") as file:
		while line := file.readline().rstrip():
			lines.append(line)
	return lines


@dataclass
class Command:
	command: list[str] = field(default_factory=list)
	output: list[str] = field(default_factory=list)


def parse_commands(input: Input) -> list[Command]:
	commands: list[Command] = []
	for line in input:
		if line[0] == '$':
			commands.append(Command())
			commands[-1].command = line[2:].split(' ')
		else:
			commands[-1].output.append(line)
	return commands


@dataclass
class File:
	name: str
	size: int


@dataclass
class Directory:
	parent: Optional["Directory"]
	directories: dict[str, "Directory"] = field(default_factory=dict)
	files: list[File] = field(default_factory=list)


def build_structure(commands: list[Command]) -> Directory:
	root = Directory(parent=None)
	cwd: Directory = root
	# Assertion = first command is cd /
	for command in commands:
		if command.command[0] == 'cd':
			target = command.command[1]
			if target == '/':
				cwd = root
			elif target == '..':
				cwd = cwd.parent
			else:
				cwd = cwd.directories[target]
			assert cwd is not None
		elif command.command[0] == 'ls':
			for line in command.output:
				size_or_dir, name = line.split(' ')
				if size_or_dir == 'dir':
					cwd.directories[name] = Directory(parent=cwd)
				else:
					cwd.files.append(File(name=name, size=int(size_or_dir)))
		else:
			raise f"Unknown command: {command.command[0]}"

	return root


Summary = dict[str, int]


def recursive_df(dir: Directory) -> Summary:
	summary: Summary = {}
	_recursive_df(dir, "", summary)
	return summary


def _recursive_df(dir: Directory, path: str, summary: Summary) -> int:
	file_size = sum([file.size for file in dir.files])
	directory_size = sum([
		_recursive_df(directory, f"{path}/{name}", summary) for name, directory in dir.directories.items()
	])
	total_size = file_size + directory_size
	summary[path if path else '/'] = total_size
	return total_size


def first_part(df: Summary) -> int:
	limit = 100_000
	return sum([
		size for path, size in df.items() if size < limit
	])


def second_part(df: Summary) -> int:
	total_size = 70_000_000
	need_available = 30_000_000
	need_available -= total_size - df['/']
	sizes = [
		size for path, size in df.items() if size >= need_available
	]
	return sorted(sizes)[0]


if __name__ == '__main__':
	input = load_input()
	commands = parse_commands(input)
	root = build_structure(commands)
	df = recursive_df(root)
	first = first_part(df)
	print(f"First: {first}")
	second = second_part(df)
	print(f"Second: {second}")
