from urllib.request import Request
from urllib.request import urlopen
import re
import os
import numpy as np

input_url:str = "https://adventofcode.com/2023/day/5/input"
example_input1:str = "./example_input1.txt"
example_answer1:int = 35
example_input2:str = example_input1
example_answer2:int = 46


def get_url_input(url:str)->list[str]:
	absolute_path = os.path.dirname(__file__)
	relative_path = "../../session_cookie"
	sessioncookie_path = os.path.join(absolute_path, relative_path)

	with open(sessioncookie_path) as f:
		req = Request(url, headers={'User-Agent':'Mozilla/5.0', 'Cookie':'session='+f.read()})

	return list(map(lambda p: str(p, encoding="utf-8").replace("\n", ""), urlopen(req).readlines()))


def get_file_input(file:str)->list[str]:
	absolute_path = os.path.dirname(__file__)
	input_path = os.path.join(absolute_path, file)

	with open(input_path) as f:
		return list(map(lambda p: p.replace("\n", ""), f.readlines()))


def compute_maps(input:list):
	p:int = 0
	while(p < len(input)):
		if "seed-to-soil" in input[p]:
			s2s_p:int = p+1
		elif "soil-to-fertilizer" in input[p]:
			s2f_p:int = p+1
			s2s_m = [[int(r) for r in in_.split()] for in_ in input[s2s_p:p-1]]
			print("computed: soil maps")
		elif "fertilizer-to-water" in input[p]:
			f2w_p:int = p+1
			s2f_m = [[int(r) for r in in_.split()] for in_ in input[s2f_p:p-1]]
			print("computed: fert maps")
		elif "water-to-light" in input[p]:
			w2l_p:int = p+1
			f2w_m = [[int(r) for r in in_.split()] for in_ in input[f2w_p:p-1]]
			print("computed: water maps")
		elif "light-to-temperature" in input[p]:
			l2t_p:int = p+1
			w2l_m = [[int(r) for r in in_.split()] for in_ in input[w2l_p:p-1]]
			print("computed: light maps")
		elif "temperature-to-humidity" in input[p]:
			t2h_p:int = p+1
			l2t_m = [[int(r) for r in in_.split()] for in_ in input[l2t_p:p-1]]
			print("computed: temp maps")
		elif "humidity-to-location" in input[p]:
			t2h_m = [[int(r) for r in in_.split()] for in_ in input[t2h_p:p-1]]
			print("computed: humid maps")
			h2l_m = [[int(r) for r in in_.split()] for in_ in input[p+1:len(input)]]
			print("computed: loc maps")
			print()
		p += 1
	
	return s2s_m, s2f_m, f2w_m, w2l_m, l2t_m, t2h_m, h2l_m


def compute_loc(input:list, part:bool):
	seed_m:list = [int(r) for r in str(str(input[0]).split(": ")[1]).split()]
	s2s_m, s2f_m, f2w_m, w2l_m, l2t_m, t2h_m, h2l_m = compute_maps(input[2:-1])
	match(part):
		case (False):
			loc_min:int = 999999999999
			for seed in seed_m:
				loc = seed2loc(seed, s2s_m, s2f_m, f2w_m, w2l_m, l2t_m, t2h_m, h2l_m)
				if loc < loc_min:
					loc_min = loc
			return loc_min
		case(True):
			loc_n:int = 0
			while(True):
				seed = loc2seed(loc_n, h2l_m, t2h_m, l2t_m, w2l_m, f2w_m, s2f_m, s2s_m)
				for seed_start, range_ in zip(*[iter(seed_m)]*2):
					if seed in range(seed_start, seed_start+range_):
						return loc_n
				loc_n += 1


def seed2loc(seed:int, s2s_m, s2f_m, f2w_m, w2l_m, l2t_m, t2h_m, h2l_m):
	return lookup_f(lookup_f(lookup_f(lookup_f(lookup_f(lookup_f(lookup_f(seed, s2s_m), s2f_m), f2w_m), w2l_m), l2t_m), t2h_m), h2l_m)


def loc2seed(loc:int, h2l_m, t2h_m, l2t_m, w2l_m, f2w_m, s2f_m, s2s_m):
	return lookup_b(lookup_b(lookup_b(lookup_b(lookup_b(lookup_b(lookup_b(loc, h2l_m), t2h_m), l2t_m), w2l_m), f2w_m), s2f_m), s2s_m)


def lookup_f(in_:list, map:list):
	for range_ in map:
		if in_ in range(range_[1], range_[1]+range_[2]):
			return range_[0] + (in_ - range_[1])
	return in_


def lookup_b(in_:list, map:list):
	for range_ in map:
		if in_ in range(range_[0], range_[0]+range_[2]):
			return range_[1] + (in_ - range_[0])
	return in_


def matrix_print(matrix:list):
	for row in matrix:
		print(str(row))


if __name__ == "__main__":
	print("PART 1")
	print()
	print("Testing...")
	print("Expected Answer: " + str(example_answer1))
	print("Computing example...")
	com_example1 = compute_loc(get_file_input(example_input1), False)
	print("Computed Example Answer: " + str(com_example1))
	assert com_example1 == example_answer1, "Example Test failed!"
	print("Example test succeeded!")
	print()
	print("Computing answer...")
	com_answer1 = compute_loc(get_url_input(input_url), False)
	print("Answer Part 1: " + str(com_answer1))
	print()
	print()
	print("PART 2")
	print()
	print("Testing...")
	print("Expected Answer: " + str(example_answer2))
	print("Computing example...")
	com_example2 = compute_loc(get_file_input(example_input2), True)
	print("Computed Example Answer: " + str(com_example2))
	assert com_example2 == example_answer2, "Example Test failed!"
	print("Example test succeeded!")
	print()
	print("Computing answer...")
	com_answer2 = compute_loc(get_url_input(input_url), True)
	print("Answer Part 2: " + str(com_answer2))
