import networkx as nx
from utility import *
import sys, argparse, os

def solve(reads):
	sequence = reads[0]
	return sequence

def main(input_file):
	reads = parse_input(input_file)
	sequence = solve(reads)
	output_file = make_file_name(input_file)
	write_output(sequence, output_file)
	return output_file



parser = argparse.ArgumentParser(description="solve hw9, cs170.")
parser.add_argument('-i', '--input', action="store", dest="input_file", help="input file", default="")
parser.add_argument('-s', '--solution', action="store", dest="solution_file", help="solution file", default="")
input_file = parser.parse_args().input_file
solution_file = parser.parse_args().solution_file
if __name__ == "__main__":
	output_file = main(input_file)
	if solution_file != "":
		check(output_file, solution_file)
	else:
		sys.exit(0)