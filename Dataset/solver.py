#import networkx as nx
from utility import *
from sets import Set
import sys, argparse, os

class solver(object):
	def __init__(self, input_file):
		self.input_file = input_file
		self.reads = parse_input(input_file)
		self.sequence = ""
		self.edges = []
		self.nodes = []
		self.edges_picked = []	#in sequence order
		self.nodes_picked = Set()

	def generate_graph():
		for read in self.reads:
			node = Node(read)
			self.nodes.append(node)
		for node1 in self.nodes:
			for node2 in self.nodes:
				if node1 is not node2:
					edge = Edge(node1, node2)
					self.edges.append(edge)
		sorted(self.edges, key=lambda edge: edge.overlap, reverse=True)

	def solve(self):
		edge_index = 0
		while len(self.nodes_picked) < len(self.nodes):
			curr_edge = self.edges[edge_index]
			edge_index += 1
			if curr_edge.first_node in self.nodes_picked and curr_edge.second_node in self.nodes_picked:

			else:
				

	def main(self):
		self.solve()
		output_file = make_file_name(self.input_file)
		write_output(self.sequence, output_file)
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