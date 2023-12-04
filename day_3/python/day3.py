from urllib.request import Request
from urllib.request import urlopen
import re
import os
import time

input_url:str = "https://adventofcode.com/2023/day/3/input"
example_input1:list = ['467..114.', '...*......', '..35..633.', '......#...', '617*......', '.....+.58.', '..592.....', '......755.', '...$.*....', '.664.598..']
example_answer1:int = 4361
example_input2:list = None
example_answer2:int = 467835


def get_input(url:str)->list[str]:
	absolute_path = os.path.dirname(__file__)
	relative_path = "../../session_cookie"
	sessioncookie_path = os.path.join(absolute_path, relative_path)

	with open(sessioncookie_path) as f:
		req = Request(url, headers={'User-Agent':'Mozilla/5.0', 'Cookie':'session='+f.read()})

	return list(map(lambda p: str(p, encoding="utf-8").replace("\n", ""), urlopen(req).readlines()))


def input2lists(input:list):
	lists:list = []
	lists = [[*line] for line in input]
	return lists


def compute_lists(lists:list):
	sum:int = 0
	starnums:list = []
	stars:list = []
	for row in range(len(lists)):
		column = 0
		while column < len(lists[row]):
			if lists[row][column].isdigit():
				num_end = column
				while(True):
					if (num_end + 1) >= len(lists[row]):
						break
					if lists[row][num_end+1].isdigit():
						num_end += 1
					else:
						break
				num = int("".join(map(str, lists[row][column:num_end+1])))

				valid, starnum = verify_surrounding(lists, row, column, num_end)
				if valid:
					sum += num
				else:
					print(str(num) + "	Row: " + str(row) + ", Start: " + str(column) + ", End: " + str(num_end) + ", Valid: " + str(valid))

				if starnum:
					print(str(num) + "	Row: " + str(row) + ", Start: " + str(column) + ", End: " + str(num_end) + ", Starnum: " + str(starnum))
					starnums.append([num, row, column, num_end])

				column = num_end

			elif lists[row][column] == "*":
				stars.append([row, column, []])

			column += 1

	return sum, starnums, stars


def verify_surrounding(lists:list, row:int, num_start:int, num_end:int):
	for r in range(row-1, row+2):
		if r < 0 or r >= len(lists):
#			print("y skip")
#			print()
			continue
#		print(lists[y])
#		print("Y: " + str(y) + ", len: " + str(len(lists[y])))
		for c in range(num_start-1, num_end+2):
#			print("X: " + str(x))
			if c < 0 or c >= len(lists[r]):
#				print("x skip")
				continue
#			print(lists[y][x])
			if lists[r][c] not in [".","1","2","3","4","5","6","7","8","9","0"]:
				if lists[r][c] == "*":
					return True, True
				return True, False
#		print()
	return False, False


def calculate_ratios(nums:list, stars:list, lists:list):
	sum_ratios:int = 0
	s = 0
	while(s < len(stars)):
#		print(stars[s])
		for r in range(stars[s][0]-1, stars[s][0]+2):
			if r < 0 or r >= len(lists[stars[s][0]]):
#				print("r skip")
				continue
			for num in nums:
				if num[1] == r:
#					print(r)
#					print(num[2], range(stars[s][1]-1, stars[s][1]+2), num[3], range(stars[s][1]-1, stars[s][1]+2))
					if num[2] in range(stars[s][1]-1, stars[s][1]+2) or num[3] in range(stars[s][1]-1, stars[s][1]+2):
#						print(num[0])
						if num[0] not in stars[s][2]:
							stars[s][2].append(num[0])
#							print("num: " + str(num[0]))
		if len(stars[s][2]) == 2:
			sum_ratios += stars[s][2][0] * stars[s][2][1]
		elif len(stars[s][2]) == 3:
			print("!!!	3er Kaktus	!!!")
#		print(stars[s][2])
		s += 1
#	print(stars)
	return sum_ratios


def matrix_print(matrix:list):
	for row in matrix:
		print(str(row))


if __name__ == "__main__":
	print("PART 1")
	print()
	print("Testing...")
	print("Expected Answer: " + str(example_answer1))
	print("Computing example...")
	lists_example = input2lists(example_input1)
	com_example = compute_lists(lists_example)
	print("Computed Example Answer: " + str(com_example[0]))
	assert com_example[0] == example_answer1, "Example Test failed!"
	print("Example test succeeded!")
	print()
	lists_answer = input2lists(get_input(input_url))
	com_sumnumsstars = compute_lists(lists_answer)
	print("Answer Part 1: " + str(com_sumnumsstars[0]))
	print()
	print()
	print("PART 2")
	print()
	print("Testing...")
	print("Expected Answer: " + str(example_answer2))
	com_example2 = calculate_ratios(com_example[1], com_example[2], lists_example)
	print("Computed Example Answer: " + str(com_example2))
	assert com_example2 == example_answer2, "Example Test failed!"
	print("Example test succeeded!")
	print()
	print("Answer Part 2: " + str(calculate_ratios(com_sumnumsstars[1], com_sumnumsstars[2], lists_answer)))