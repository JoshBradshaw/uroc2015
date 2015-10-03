from pprint import pprint
import re

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

if __name__ == '__main__':
    spectrums = read_mdf('test.mgf')
    pprint(spectrums[0][0])
    pprint(spectrums[0][1])


