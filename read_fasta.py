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
        peptides[key] = sep_peptides(proteins[key])

    print peptides.items()

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
