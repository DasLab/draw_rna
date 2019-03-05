import draw_rna as d
import argparse
import sys
import os

color = {'A': 'y', 'U':'b', 'G':'r', 'C':'g', 'T': 'b', 'N': 'k', ' ': 'w'}

def seq2col(seq):
    col = []
    for c in seq:
        col.append(color[c])
    return col


def main():
    p = argparse.ArgumentParser()
    p.add_argument('inputfile')
    p.add_argument('--png', action='store_true')
    p.add_argument('--line', action='store_true')
    args = p.parse_args()

    with open(args.inputfile) as f:
        for line in f:
            if not line.startswith('#') and line.strip() != '':
                try:
                    name = line.strip().replace(' ', '_')
                    seq = next(f).strip()
                    secstruct = next(f).strip()
                except Exception as e:
                    print e
                    raise ValueError('improper format')
    
                try:
                    col = next(f).strip()
                except:
                    col = None
    
                print 'drawing %s' % name
                if col:
                    d.draw_rna(seq, secstruct, col, name, line=args.line)
                else:
                    d.draw_rna(seq, secstruct, seq2col(seq), name, line=args.line)
                
                if args.png:
                    if 'INKSCAPEDIR' not in os.environ:
                        print('Please set INKSCAPEDIR environmental variable with path to Inkscape app.')
                        return
                    inkscape = '%s/Contents/Resources/bin/inkscape' % os.environ['INKSCAPEDIR']
                    if not os.path.isfile(inkscape):
                        print('Inkscape not found. Please update INKSCAPEDIR environmental variable with path to Inkscape app.')
                        return
                    os.system('%s --export-png $(pwd)/%s.png $(pwd)/%s.svg' % (inkscape, name, name))
                    os.system('rm $(pwd)/%s.svg' % (name))



if __name__ == '__main__':
    main()
