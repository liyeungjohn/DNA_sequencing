#import networkx as nx
from utility import *
#from sets import Set
import sys, argparse, os

class solver(object):
	def __init__(self, input_file):
		self.input_file = input_file
		self.reads = parse_input(input_file)
		self.sequence = ""
		self.edges = []
		self.nodes = []
		self.nodes_picked = 0
		self.edges_cc = []
		self.nodes_cc = []

	def generate_graph(self):
		for read in self.reads:
			node = Node(read)
			self.nodes.append(node)
			#print len(node.read)
		for index1 in range(len(self.nodes)):
			for index2 in range(len(self.nodes)):
				if index2 > index1:
					edge = Edge(self.nodes[index1], self.nodes[index2])
					self.edges.append(edge)
		sorted(self.edges, key=lambda edge: edge.overlap, reverse=True)
		#for edge in self.edges:
			#print "first: " + edge.first_node.read + " second: " + edge.second_node.read + " overlap: " + str(edge.overlap) + " str:" + edge.overlap_string

	def solve(self):
		edge_index = 0
		while self.nodes_picked < len(self.nodes) and edge_index < len(self.edges):
			curr_edge = self.edges[edge_index]
			edge_index += 1
			first_node = curr_edge.first_node
			second_node = curr_edge.second_node
			first_cc_index = -1
			second_cc_index = -1
			bad = False 
			cc_index = 0
			for nodes in self.nodes_cc:
				if first_node in nodes:
					if first_node.read == nodes[len(nodes) - 1].read:
						first_cc_index = cc_index
					else:
						bad = True
						break
				if second_node in nodes:
					if second_node.read == nodes[0].read:
						second_cc_index = cc_index
					else: 
						bad = True
						break
				cc_index += 1
			if bad:
				continue
			if first_cc_index != -1 and second_cc_index != -1:
				#nodes_cc
				first_nodes_cc = self.nodes_cc[first_cc_index]
				second_nodes_cc = self.nodes_cc.pop(second_cc_index)
				first_nodes_cc.extend(second_nodes_cc)
				#edges_cc
				first_edges_cc = self.edges_cc[first_cc_index]
				second_edges_cc = self.edges_cc.pop(second_cc_index)
				first_edges_cc.append(curr_edge)
				first_edges_cc.extend(second_edges_cc)
			if first_cc_index != -1 and second_cc_index == -1:
				self.nodes_cc[first_cc_index].append(second_node)
				self.edges_cc[first_cc_index].append(curr_edge)
				self.nodes_picked += 1
			if first_cc_index == -1 and second_cc_index != -1:
				self.nodes_cc[second_cc_index].insert(0, first_node)
				self.edges_cc[second_cc_index].insert(0, curr_edge)
				self.nodes_picked += 1
			if first_cc_index == -1 and second_cc_index == -1:
				self.nodes_cc.append([first_node, second_node])
				self.edges_cc.append([curr_edge])
				self.nodes_picked += 2

	def generate_sequence(self):
		if len(self.edges_cc) > 1:
			print "shit more than 1 cc!"
		cc_index = 0
		self.sequence = ""
		for edge_cc in self.edges_cc:
			cur_sequence = self.edges_cc[cc_index][0].first_node.read
			for edge in self.edges_cc[cc_index]:
				to_add = edge.second_node.read[edge.overlap:]
				cur_sequence += to_add
			self.sequence += cur_sequence


	def main(self):
		self.generate_graph()
		self.solve()
		self.generate_sequence()
		output_file = make_file_name(self.input_file)
		print "sequence:" + self.sequence
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