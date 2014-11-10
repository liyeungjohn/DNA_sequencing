import hashlib, sys

def parse_input(file1):
	reads = []
	f = open(file1, 'r')
	read = f.readline()
	while read != "":
		if read not in reads:
			reads.append(read)
		read = f.readline()
	f.close()
	return reads

def write_output(output, file2):
	f = open(file2, 'w')
	f.write(output + "\n")
	f.close()

def check(file1, file2):
	if files_are_the_same(file1, file2):
		print("Passed")
		sys.exit(0)
	else:
		print("Failed")
		sys.exit(1)

def files_are_the_same(file1, file2):
    return md5sum(file1) == md5sum(file2)

def make_file_name(file1):
	return "john_" + file1

def md5sum(filename, block_size=2**20):
    f = open(filename, "rb")
    md5 = hashlib.md5()
    while True:
        data = f.read(block_size)
        if not data:
            break
        md5.update(data)
    f.close()
    return md5.digest()


class Node(object):

	def __init__(self, read):
		self.read = read

	@staticmethod
	def cal_overlap(node1, node2):
		#first direction:
		overlap1, overlap_string1 = Node.cal_overlap_d(node1.read, node2.read)
		#second direction:
		overlap2, overlap_string2 = Node.cal_overlap_d(node2.read, node1.read)
		if overlap1 > overlap2:
			return node1, node2, overlap1, overlap_string1
		else:
			return node2, node1, overlap2, overlap_string2

	#direction: end of node1 overlap with start of node2
	#read1_string
	#		read2_string
	@staticmethod
	def cal_overlap_d(read1, read2):
		#truncate useless front of read1 if read1 is larger than read2
		if len(read1) > len(read2):
			read1 = read1[(len(read1)-len(read2)):]
		if len(read1) == 1:
			if read1 == read2[0]:
				return 1, read1
			else:
				return 0, ""
		#check best case of read1 entirely overlapping with read2
		if read1 == read2[:len(read1)]:
			return len(read1), read1
		else:
			return Node.cal_overlap_d(read1[1:], read2)


class Edge(object):
	#first_node, second_node, overlap, overlap_string
	def __init__(self, node1, node2):
		self.first_node, self.second_node, self.overlap, self.overlap_string = Node.cal_overlap(node1, node2)

#node1, node2, overlap, overlap_string = Node.cal_overlap(Node("TGCCTCGAACTTTCCCGTACCACAG"), Node("TGCCTCGAACTTTCCCGTACCACAGGATTCACGTT"))
#print node1.read + "\n" + node2.read + "\n" + str(overlap) + "\n" + overlap_string