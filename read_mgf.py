"""
De Nova Peptide Sequencing

Usage:
  pepseq <spectrum_mgf_file> <protein_fasta_file>
"""

from read_fasta import readFasta
from pprint import pprint
import re
from docopt import docopt

def read_peptides(filename):
    peptides = {}
    f = open(filename,'rU')
    for line in f:
        line = line.strip()
        key_val_pair = line.split(' ')
        peptides[key_val_pair[0]] = float(key_val_pair[1])
    
    return peptides

def read_mdf(fp):
    """Parse the MGF file of protein spectrums"""
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
                        if '.' in value:
                            metadata[label] = float(value)
                        else:
                            metadata[label] = int(value)
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

def mass_yions(peptide_string):
    y_ion_masses = []
    ion_mass = sum(fn_mass[peptide] for peptide in peptide_string)
    for ii in xrange(0, len(peptide_string)-1):
        ion_mass -= fn_mass[peptide_string[ii]]
        y_ion_masses.append(ion_mass + 19.018)
    return y_ion_masses

def mass_bions(peptide_string):
    b_ion_masses = []
    ion_mass = sum(fn_mass[peptide] for peptide in peptide_string)
    for ii in xrange(len(peptide_string)-1, 1, -1):
        ion_mass -= fn_mass[peptide_string[ii]]
        b_ion_masses.append(ion_mass + 19.018)
    return b_ion_masses

def score_candidate(peptide_string,spectrum):
    y_ions = mass_yions(peptide_string)
    score = 0
    for mass,intensity in spectrum:
        for y_mass in y_ions:
            if abs(y_mass - mass) < 0.5:
                score += 1
                continue
    return score

def score_candidate_with_b(peptide_string,spectrum):
    ions = mass_yions(peptide_string)
    ions += mass_bions(peptide_string)
    score = 0
    for mass,intensity in spectrum:
        for ion_mass in ions:
            if abs(ion_mass - mass) < 0.5:
                score += 1
                continue
    return score

def choose_candidates(candidates,spectrum):
        score = {}
        for candidate in candidates:
            score[candidate] = score_candidate_with_b(candidate, spectrum)
        max_score = -1
        selected = ""
        for candidate in score:
            if score[candidate] > max_score:
                    max_score = score
                selected = candidate
        return selected


if __name__ == '__main__':
    arguments = docopt(__doc__)
    read_fasta(arguments["<protein_fasta_file>"])

    spectrums = read_mdf(arguments["<spectrum_mgf_file>"])
    peptides = read_peptides('peptides.txt')
    candidates = {}
    chosen_candidate = {}
    z_values = []
    mass = []
    count  = 0
    for metadata, spectrum in spectrums:
        charge = calc_charge(metadata)
        z_values.append(charge)
        m = calc_mass(metadata,charge)
        scan_number = metadata['SCANS']
        mass.append(m)
        candidates[scan_number] = find_candidates(peptides,m)
        chosen_candidate[scan_number] = choose_candidates(candidates[scan_number],spectrum)
    
    outf = open('spectrum-protein-matches.txt','w')

    for scan_number in chosen_candidate:
        outf.write(str(scan_number) + ' ' + chosen_candidate[scan_number] + '\n')

