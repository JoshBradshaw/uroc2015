import sys
import re
from collections import defaultdict

proteins = {}
peptides = defaultdict(list)

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
		peptides[key] = re.findall(r'[RK](?!P)',proteins[key])

	print peptides.items()


def main():
	readFasta(sys.argv[1])

if __name__ == '__main__':
	main()
