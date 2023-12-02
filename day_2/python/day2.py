from urllib.request import Request
from urllib.request import urlopen
import re
import os

input_url:str = "https://adventofcode.com/2023/day/2/input"
example_input1:list = ['Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green', 'Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue', 'Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red', 'Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red', 'Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green']
example_answer1:int = 8
example_input2:list = example_input1
example_answer2:int = 2286


def get_input(url:str)->list[str]:
	absolute_path = os.path.dirname(__file__)
	relative_path = "../../session_cookie"
	sessioncookie_path = os.path.join(absolute_path, relative_path)

	with open(sessioncookie_path) as f:
		req = Request(url, headers={'User-Agent':'Mozilla/5.0', 'Cookie':'session='+f.read()})

	return list(map(lambda p: str(p, encoding="utf-8"), urlopen(req).readlines()))


def compute_games(input:list):
	sum_valid:int = 0
	sum_power:int = 0
	for line in input:
		min_red:int = -1
		min_green:int = -1
		min_blue:int = -1
		game_id = int(re.findall('\d+', line)[0])
		game = line.split(": ")[1]
		pulls = game.split(";")
		valid:bool = True
		for pull in pulls:
			colors = pull.split(", ")
			for color in colors:
				if "red" in color:
					cubes_red = int(re.findall('\d+', color)[0])
					if cubes_red > min_red:
						min_red = cubes_red
					if cubes_red > 12 and valid:
						valid = False
				elif "green" in color:
					cubes_green = int(re.findall('\d+', color)[0])
					if cubes_green > min_green:
						min_green = cubes_green
					if cubes_green > 13 and valid:
						valid = False
				elif "blue" in color:
					cubes_blue = int(re.findall('\d+', color)[0]) 
					if cubes_blue > min_blue:
						min_blue = cubes_blue
					if cubes_blue > 14 and valid:
						valid = False

		if valid:
			print("game: " + str(game_id) + " is valid: +1")
			sum_valid += game_id
		
		power = min_red * min_green * min_blue
		print("Power: " + str(power))
		sum_power += power

	return sum_valid, sum_power


if __name__ == "__main__":
	print("Computing example...")
	print("Example Input: " + str(example_input1))
	com_example = compute_games(example_input1)
	print()
	print("Computing input Part 1&2...")
	computed_games = compute_games(get_input(input_url))
	print()
	print()
	print("PART 1")
	print()
	print("Testing...")
	print("Expected Answer: " + str(example_answer1))
	print("Computed Example Answer: " + str(com_example[0]))
	assert com_example[0] == example_answer1, "Example Test failed!"
	print("Example test succeeded!")
	print()
	print("Answer Part 1: " + str(computed_games[0]))
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
	print("Answer Part 1: " + str(computed_games[1]))