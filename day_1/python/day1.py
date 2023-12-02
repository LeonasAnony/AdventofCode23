from urllib.request import Request
from urllib.request import urlopen
import re
import os
import time

input_url:str = "https://adventofcode.com/2023/day/1/input"
example_input1:list = ['1abc2', 'pqr3stu8vwx', 'a1b2c3d4e5f', 'treb7uchet']
example_answer1:int = 142
example_input2:list = ['two1nine', 'eightwothree', 'abcone2threexyz', 'xtwone3four', '4nineeightseven2', 'zoneight234', '7pqrstsixteen']  
example_answer2:int = 281


def get_input(url:str)->list[str]:
	absolute_path = os.path.dirname(__file__)
	relative_path = "../../session_cookie"
	sessioncookie_path = os.path.join(absolute_path, relative_path)

	with open(sessioncookie_path) as f:
		req = Request(url, headers={'User-Agent':'Mozilla/5.0', 'Cookie':'session='+f.read()})

	return list(map(lambda p: str(p, encoding="utf-8"), urlopen(req).readlines()))


def replace_digits(lines:list)->list[str]:
	new_lines:list = []
	for line in lines:
		line = line.replace("one", "one1one").replace("two", "two2two").replace("three", "three3three").replace("four", "four4four").replace("five", "five5five").replace("six", "six6six").replace("seven", "seven7seven").replace("eight", "eight8eight").replace("nine", "nine9nine")
		new_lines.append(line)

	return new_lines


def get_sum(lines:list)->int:
	sum:int = 0
	for line in lines:
		nums = re.findall('\d', line)
		sum += int(nums[0] + nums[-1])

	return sum


if __name__ == "__main__":
	print("PART 1")
	print()
	print("Testing...")
	print("Example Input: " + str(example_input1))
	print("Expected Answer: " +str(example_answer1))
	com_example1 = get_sum(example_input1)
	print("Computed Example Answer: " + str(com_example1))
	assert com_example1 == example_answer1, "Example Test failed!"
	print("Example test succeeded!")
	print()
	print("Computing part 1...")
	print("Answer Part 1: " + str(get_sum(get_input(input_url))))
	print()
	print()
	print("PART 2")
	print()
	print("Testing...")
	print("Example Input: " + str(example_input2))
	print("Expected Answer: " + str(example_answer2))
	com_example2 = get_sum(replace_digits(example_input2))
	print("Computed Example Answer: " + str(com_example2))
	assert com_example2 == example_answer2, "Example Test failed!"
	print("Example test succeeded!")
	print()
	print("Computing part 2...")
	print("Answer Part 2: " + str(get_sum(replace_digits(get_input(input_url)))))