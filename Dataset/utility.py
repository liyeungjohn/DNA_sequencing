import hashlib, sys

def parse_input(file1):
	reads = []
	f = open(file1, 'r')
	read = f.readline()
	while read != "":
		reads.append(read)
		read = f.readline()
	f.close()
	return reads

def write_output(output, file2):
	f = open(file2, 'w')
	f.write(output)
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
	def __init__(self):
		self.self = self

