task = '25'
TEST = """1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122""".split('\n')

snafu = {'0': 0, '1': 1, '2': 2, '-': -1, '=': -2}
decimal = {value: key for key, value in snafu.items()}
mul = 5


def load_file() -> list[str]:
	lines = []
	with open(f'{task}.in') as file:
		while line := file.readline().rstrip():
			lines.append(line)
	return lines


def to_snafu(num: int) -> str:
	res = []
	while num:
		num, cur = divmod(num, mul)
		if cur > 2:
			num += 1
			cur -= 5
		res.append(decimal[cur])
	return ''.join(reversed(res))


def to_decimal(input: str) -> int:
	current_mul = 1
	res = 0
	for i in range(len(input) - 1, -1, -1):
		res += snafu[input[i]] * current_mul
		current_mul *= mul
	return res


def first_part(input: list[str]) -> str:
	return to_snafu(sum(to_decimal(line) for line in input))


if __name__ == '__main__':
	input = load_file()
	for line in input:
		assert to_snafu(to_decimal(line)) == line
	first = first_part(input)
	print(f'First part {first}')