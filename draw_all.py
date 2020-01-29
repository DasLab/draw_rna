import draw_rna as d
import argparse
import sys
import numpy as np
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
    p.add_argument('--color_values', nargs='*', action='store', dest='color_value_file', help='File containing values (i.e. reactivities)')
    args = p.parse_args()

    print(args)

    ext_color_file=False
    construct_counter = 0

    with open(args.inputfile) as f:
        for line in f:
            if not line.startswith('#') and line.strip() != '':
                try:
                    name = line.strip().replace(' ', '_')
                    seq = next(f).strip()
                    secstruct = next(f).strip()
                except Exception as e:
                    print(e)
                    raise ValueError('improper format')
                try:
                    color_string = next(f).strip()
                    print('got col ,%s,' % color_string)
                except:
                    color_string = None
        
                print('drawing %s' % name)

                if args.color_value_file is not None:
                    print('Reading in colors from %s' % args.color_value_file[construct_counter])
                    color_vec = np.loadtxt(args.color_value_file[construct_counter])
                    ext_color_file=True
                    assert(len(color_vec) == len(seq))

                if ext_color_file:
                    d.draw_rna(seq, secstruct, color_vec, name, line=args.line, ext_color_file=ext_color_file, 
                        cmap_name='gist_heat_r', chemical_mapping_mode=True)
                elif color_string:
                    d.draw_rna(seq, secstruct, color_string, name, line=args.line)
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
                construct_counter+=1



if __name__ == '__main__':
    main()
