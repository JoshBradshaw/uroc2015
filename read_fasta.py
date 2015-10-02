import sys

proteins = {}

def readFasta(filename):
	inf = open(filename,'rU')
	name = ""
	dna = ""
	for line in inf:
		if line[0] == '>':
			if name != "" :
				proteins[name] = dna
			name = line[1:]
			dna = ""
		else : 
			dna += line

	for key in proteins:
		print "key: " + key + " val: " + proteins[key]


def main():
	readFasta(sys.argv[1])

if __name__ == '__main__':
	main()
