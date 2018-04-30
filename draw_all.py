import draw_rna as d
import argparse
import sys
import os

p = argparse.ArgumentParser()
p.add_argument('inputfile')
args = p.parse_args()

color = {'A': 'y', 'U':'b', 'G':'r', 'C':'g', 'T': 'b', 'N': 'e', ' ': 'w'}
def seq2col(seq):
    col = []
    for c in seq:
        col.append(color[c])
    return col

with open(args.inputfile) as f:
    for line in f:
        if not line.startswith('#') and line.strip() != '':
            try:
                name = line.strip()
                seq = next(f).strip()
                secstruct = next(f).strip()
            except Exception as e:
                print e
                raise ValueError('improper format')

            try:
                col = next(f).strip()
            except:
                col = False

            print 'drawing %s' % name
            if col:
                d.draw_rna(seq, secstruct, col, name)
            else:
                d.draw_rna(seq, secstruct, seq2col(seq), name)
