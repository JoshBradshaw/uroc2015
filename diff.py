import sys
import csv
from pprint import pprint

candidates = {}

def compare(csvfile, candidatesfile):
	inf = open(candidatesfile,'rU')
	count = 0
	for line in inf:
		line = line.strip()
		pair = line.split(' ')
		if len(pair) == 2:
			candidates[int(pair[0])] = pair[1]
	incsv = open(csvfile,'r')
	reader = csv.DictReader(incsv)
	row_count = 0
	for row in reader:
		row_count += 1
		if int(row['Scan']) in candidates.keys():
			if row['Peptide'].replace('(+57.02)','') == candidates[int(row['Scan'])]:
				count += 1
	print count, row_count
	

def main():
	compare('test.peaksdb.csv',sys.argv[1])

if __name__ =='__main__':
	main()
