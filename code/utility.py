import hashlib, sys, fileinput
def parse_input():
	reads = []
	for line in fileinput.input():
		line = line.strip()
		reads.append(line)
	return filter_reads(reads)

def filter_reads(reads):
	result = []
	for index1 in range(len(reads)):
		duplicate = False
		read1 = reads[index1]
		for index2 in range(len(reads)):
			if index2 != index1:
				if read1 in reads[index2]:
					duplicate = True
		if not duplicate:
			result.append(read1)
	return result

def cal_overlap(read1, read2):
	#first direction:
	overlap1, overlap_string1 = cal_overlap_d(read1, read2)
	#second direction:
	overlap2, overlap_string2 = cal_overlap_d(read2, read1)
	if overlap1 > overlap2:
		return read1, read2, overlap1, overlap_string1
	else:
		return read2, read1, overlap2, overlap_string2

#direction: end of node1 overlap with start of node2
#read1_string
#		read2_string

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
		return cal_overlap_d(read1[1:], read2)


class Edge(object):
	#first_node, second_node, overlap, overlap_string
	def __init__(self, first, second, directed):
		if directed:
			self.first = first
			self.second = second
			self.overlap, self.overlap_string = cal_overlap_d(first, second)
		else:			
			self.first, self.second, self.overlap, self.overlap_string = cal_overlap(first, second)
