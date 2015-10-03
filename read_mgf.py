from pprint import pprint
import re

def read_peptides(filename):
	peptides = {}
	f = open(filename,'rU')
	for line in f:
		line = line.strip()
		key_val_pair = line.split(' ')
		peptides[key_val_pair[0]] = float(key_val_pair[1])
	
	return peptides

def read_mdf(fp):
    metadata = {}
    spectrums = []
    with open(fp, 'r') as f:
        for line in f:
            line = line.strip()
            if line=="BEGIN IONS":
                spectrum = []
                metadata = {}
            if line=="END IONS":
                spectrums.append( (metadata, spectrum) )

            if line:
                if line.count('=') == 1:
                    label, value = line.split('=')
                    if not label == 'CHARGE':
                        metadata[label] = float(value)
                    else:
                        metadata[label] = value
                elif line[0].isdigit():
                    mass, intensity = line.split(' ')
                    spectrum.append( (float(mass), float(intensity)) )
                else:
                    pass
    return spectrums


fn_mass = {'A':71.03711, 'R':156.10111,'N':114.04293,'D':115.02694,'C':160.08919,'E':129.04295,'Q':128.05858,'G':57.02146,'H':137.05891,'I':113.08406,'L':113.08406,'K':128.09496,'M':131.04049,'F':147.06841,'P':97.0256,'S':87.3203,'T':101.04768,'W':186.07931,'Y':163.06333,'V':99.06841}

def calc_charge(metadata):
	return int(metadata['CHARGE'][0])

def calc_mass(metadata,charge):
	pep_mass = metadata['PEPMASS']
	mass = (pep_mass - 1.007)*charge - 18.01
	return mass

def find_candidates(peptides,mass):
	candidates = []
	for peptide in peptides:
		if abs(peptides[peptide] - mass) < 0.5 :
			candidates.append(peptide)
	
	return candidates


if __name__ == '__main__':
    spectrums = read_mdf('test.mgf')
    peptides = read_peptides('peptides.txt')
    z_values = []
    mass = []
    count  = 0
    for metadata, spectrum in spectrums:
	    charge = calc_charge(metadata)
	    z_values.append(charge)
	    m = calc_mass(metadata,charge)
	    mass.append(m)
	    candidates = find_candidates(peptides,m)
	    if candidates == []:
		    count+=1
    print count


