import sys
import re
from collections import defaultdict

proteins = {}
peptides = defaultdict(list)

peptides_mass = {}

fn_mass = {'A':71.03711, 'R':156.10111,'N':114.04293,'D':115.02694,'C':160.08919,'E':129.04295,'Q':128.05858,'G':57.02146,'H':137.05891,'I':113.08406,'L':113.08406,'K':128.09496,'M':131.04049,'F':147.06841,'P':97.0256,'S':87.3203,'T':101.04768,'W':186.07931,'Y':163.06333,'V':99.06841}

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
		peptides[key] = sep_peptides(proteins[key])

	calc_peptides_mass()

	for peptide in peptides_mass:
		print "peptide: " + peptide +  " mass: " + str(peptides_mass[peptide]) + "\n"

def mass(peptide):
	total_mass = 0.0
	for p in peptide:
		total_mass += fn_mass[p]
	return total_mass

def calc_peptides_mass():
	for key in peptides:
		for peptide in peptides[key]:
			peptides_mass[peptide] = mass(peptide)

def sep_peptides(peptide): 
    peptides = []
    split_matches = re.finditer(r'[RK](?!P)', peptide)
    prev_split_location = 0
    for m in split_matches:
        split_location = m.end()
        peptides.append(peptide[prev_split_location:split_location])
        prev_split_location = split_location
    return peptides

def main():
	readFasta(sys.argv[1])

if __name__ == '__main__':
	main()
