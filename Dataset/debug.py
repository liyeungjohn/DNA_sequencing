from solver import *
from utility import *
import unittest

class TestUtility(unittest.TestCase):

	def test_filter_reads(self):
		list1 = ["ACT", "ACTG", "AC", "A"]
		filtered1 = filter_reads(list1)
		self.assertEqual(filtered1, ["ACTG"])


class TestSolver(unittest.TestCase):

	def test_filter_reads1(self):
		reads1 = ["ACTG", "TGCA", "ACAC", "TTTT", "GGGG"]
		solver1 = solver(reads1)
		solver1.reads = reads1
		solver1.main()
		solver1.print_nodes()
		for read in reads1:
			good = False
			for node in solver1.nodes:
				if node.read == read:
					good = True
			self.assertTrue(good)
		#solver1.print_edges()
		#solver1.print_sequence()


if __name__ == "__main__":
	unittest.main()