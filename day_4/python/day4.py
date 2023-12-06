from urllib.request import Request
from urllib.request import urlopen
import re
import os
import numpy as np

input_url:str = "https://adventofcode.com/2023/day/4/input"
example_input1:list = ['Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53', 'Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19', 'Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1', 'Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83', 'Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36', 'Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11']
example_answer1:int = 13
example_input2:list = None
example_answer2:int = 30


def get_input(url:str)->list[str]:
	absolute_path = os.path.dirname(__file__)
	relative_path = "../../session_cookie"
	sessioncookie_path = os.path.join(absolute_path, relative_path)

	with open(sessioncookie_path) as f:
		req = Request(url, headers={'User-Agent':'Mozilla/5.0', 'Cookie':'session='+f.read()})

	return list(map(lambda p: str(p, encoding="utf-8").replace("\n", ""), urlopen(req).readlines()))


def input2cards(input:list):
	"""
	cards:list struct:
		cards:[card:[win_nums:[int, ...], nums:[int, ...], copies:int, matches:int], ...]
		cards[i] -> card:[[], []]
		cards[i][0] -> win_nums:[int, ...]
		cards[i][1] -> nums:[int, ...]
		cards[i][2] -> copies:int
		cards[i][3] -> matches:int
	"""
	cards:list = []
	for card in input:
		card = str(card.split(": ")[1]).split(" | ")
		cards.append([str(card[0]).split(), str(card[1]).split(), 1, None])
	return cards


def compute_matches_points(card:list):
	matches:int = 0
	for win_num in card[0]:
		if win_num in card[1]:
			matches += 1
	if matches == 1:
		points:int = 1
	elif matches > 1:
		points:int = 2**(matches-1)
	else:
		points:int = 0

	return matches, points


def compute_cards(cards:list):
	point_sum:int = 0
	c:int = 1
	while c <= len(cards):
		matches, points = compute_matches_points(cards[c-1])
		point_sum += points
		cards[c-1][3] = matches
		copy:int = 0
		while(copy < cards[c-1][2]):
			for m in range(matches):
				cards[c+m][2] += 1
			copy += 1
		c += 1

	copy_sum:int = np.sum([card[2] for card in cards], 0)

	return point_sum, copy_sum


def matrix_print(matrix:list):
	for row in matrix:
		print(str(row))


if __name__ == "__main__":
	print("PART 1")
	print()
	print("Testing...")
	print("Expected Answer: " + str(example_answer1))
	print("Computing example...")
	cards_example = input2cards(example_input1)
	com_example = compute_cards(cards_example)
	print("Computed Example Answer: " + str(com_example[0]))
	assert com_example[0] == example_answer1, "Example Test failed!"
	print("Example test succeeded!")
	print()
	cards_answer = input2cards(get_input(input_url))
	com_answer = compute_cards(cards_answer)
	print("Answer Part 1: " + str(com_answer[0]))
	print()
	print()
	print("PART 2")
	print()
	print("Testing...")
	print("Expected Answer: " + str(example_answer2))
	print("Computed Example Answer: " + str(com_example[1]))
	assert com_example[1] == example_answer2, "Example Test failed!"
	print("Example test succeeded!")
	print()
	print("Answer Part 2: " + str(com_answer[1]))