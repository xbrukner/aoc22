task = '01'

Input = list[list[int]]


def load_input() -> Input:
    numbers: Input = [[]]
    with open(f"{task}.in") as file:
        while line := file.readline():
            if line == '\n':
                numbers.append([])
            else:
                numbers[-1].append(int(line))
    return numbers


def first_part(input: Input):
    max_sum = max([sum(elf) for elf in input])
    print(f"Largest sum count: {max_sum}")


def second_part(input: Input):
    sums = [sum(elf) for elf in input]
    sums.sort(reverse=True)
    top_three = sum(sums[0:3])
    print(f"Top three sum: {top_three}")


if __name__ == '__main__':
    input_list = load_input()
    first_part(input_list)
    second_part(input_list)
