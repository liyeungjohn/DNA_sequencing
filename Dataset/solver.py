import networkx as nx
from utility import *
import sys, argparse, os

class solver(object):
	def __init__(self, input_file):
		self.reads = parse_input(input_file)
		self.graph = None

	def solve(self):
		sequence = self.reads[0]
		return sequence

	def main(self):
		sequence = self.solve()
		output_file = make_file_name(input_file)
		write_output(sequence, output_file)
		return output_file


#parse input
parser = argparse.ArgumentParser(description="solve hw9, cs170.")
parser.add_argument('-i', '--input', action="store", dest="input_file", help="input file", default="")
parser.add_argument('-s', '--solution', action="store", dest="solution_file", help="solution file", default="")
input_file = parser.parse_args().input_file
solution_file = parser.parse_args().solution_file

#main logic
if __name__ == "__main__":
	output_file = solver(input_file).main()
	if solution_file != "":
		check(output_file, solution_file)
	else:
		sys.exit(0)