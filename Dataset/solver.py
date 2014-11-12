from utility import *
#from sets import Set
import sys, argparse, os, logging

class solver(object):
	def __init__(self, reads):
		self.reads = reads
		self.sequence = ""
		self.edges = []	#all edges with overlap > 0
		self.nodes_picked = 0
		self.edges_cc = []
		self.nodes_cc = []

	def generate_graph(self):
		for index1 in range(len(self.reads)):
			for index2 in range(len(self.reads)):
				if index2 > index1:
					edge = Edge(self.reads[index1], self.reads[index2])
					self.edges.append(edge)
		self.edges = sorted(self.edges, key=lambda edge: edge.overlap, reverse=True)

	def solve(self):
		edge_index = 0
		while self.nodes_picked < len(self.reads) and edge_index < len(self.edges):
			curr_edge = self.edges[edge_index]
			edge_index += 1
			first = curr_edge.first
			second = curr_edge.second
			first_cc_index = -1
			second_cc_index = -1
			bad = False 
			cc_index = 0
			for nodes in self.nodes_cc:
				if first in nodes:
					if first == nodes[len(nodes) - 1]:
						first_cc_index = cc_index
					else:
						bad = True
						break
				if second in nodes:
					if second == nodes[0]:
						second_cc_index = cc_index
					else: 
						bad = True
						break
				cc_index += 1
			if bad:
				continue
			if first_cc_index != -1 and second_cc_index != -1:
				if first_cc_index == second_cc_index:
					continue
				else:
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
				self.nodes_cc[first_cc_index].append(second)
				self.edges_cc[first_cc_index].append(curr_edge)
				self.nodes_picked += 1
			if first_cc_index == -1 and second_cc_index != -1:
				self.nodes_cc[second_cc_index].insert(0, first)
				self.edges_cc[second_cc_index].insert(0, curr_edge)
				self.nodes_picked += 1
			if first_cc_index == -1 and second_cc_index == -1:
				self.nodes_cc.append([first, second])
				self.edges_cc.append([curr_edge])
				self.nodes_picked += 2

	def generate_sequence(self):
		if len(self.edges_cc) > 1:
			logging.debug("shit more than 1 cc!")

		result_edges = []
		for index in range(len(self.edges_cc) - 1):
			last_edge = self.edges_cc[index][-1]
			next_edge = self.edges_cc[index + 1][0]
			new_edge = Edge(last_edge.second, next_edge.first)
			result_edges.extend(self.edges_cc[index])
			result_edges.append(new_edge)
		result_edges.extend(self.edges_cc[-1])

		cc_index = 0
		self.sequence = ""
		for edge_cc in self.edges_cc:
			cur_sequence = self.edges_cc[cc_index][0].first
			for edge in self.edges_cc[cc_index]:
				to_add = edge.second[edge.overlap:]
				cur_sequence += to_add
			self.sequence += cur_sequence

	def main(self):
		self.generate_graph()
		self.solve()
		self.generate_sequence()
		self.print_reads()
		self.print_edges()
		self.print_nodes_cc()
		self.print_edges_cc()
		self.print_sequence()
		print self.sequence

	#for debugging:
	def print_reads(self):
		logging.debug("print_reads")
		for read in self.reads:
			logging.debug("read: " + read)

	def print_edges(self):
		logging.debug("print_edges")
		for edge in self.edges:
			logging.debug("edge.first: " + edge.first + " 	second: " + edge.second)
			logging.debug("edge.overlap: " + str(edge.overlap) + "		overlap_string: " + edge.overlap_string)

	def print_nodes_cc(self):
		logging.debug("print_nodes_cc")
		for node_cc in self.nodes_cc:
			logging.debug("next_cc")
			for node in node_cc:
				logging.debug("node.read: " + node)

	def print_edges_cc(self):
		logging.debug("print_edges_cc")
		for edge_cc in self.edges_cc:
			logging.debug("next_cc")
			for edge in edge_cc:
				logging.debug("edge.first: " + edge.first + " 	second: " + edge.second)
				logging.debug("edge.overlap: " + str(edge.overlap) + "		overlap_string: " + edge.overlap_string)

	def print_sequence(self):
		logging.debug("sequence: " + self.sequence)

#logging configs
logging.basicConfig(filename="run.log", level=logging.DEBUG)

#main logic
if __name__ == "__main__":
	solver(parse_input()).main()
	sys.exit(0)