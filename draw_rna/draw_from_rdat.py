from RDATKit import rdatkit
import draw_rna.draw as d
import sys,os
import argparse
import numpy as np

def draw_rdat_construct(rdat_file, construct_id):


    rdat_identifier=os.path.basename(rdat_file).replace('.rdat','')
    
    rdat = rdatkit.RDATFile()

    # load RDAT file
    rdat.load(open(rdat_file))

    seqpos = [x-1 for x in rdat.constructs['EteRNA Cloud Lab'].seqpos]
    seq=rdat.constructs['EteRNA Cloud Lab'].data[construct_id].annotations['sequence'][0]
    secstruct = rdat.constructs['EteRNA Cloud Lab'].data[construct_id].annotations['structure'][0]

    assert len(seq) == len(secstruct)

    reactivities = rdat.constructs['EteRNA Cloud Lab'].data[construct_id].values

    reactivities.extend([0]*(len(seq) - len(reactivities)))
    name = '%s_%d' % (os.path.basename(rdat_identifier), construct_id)
    print('Drawing construct:')
    print(seq)
    print(secstruct)
    print(name)
    d.draw_rna(seq, secstruct, np.array(reactivities), filename=name, ext_color_file=True, cmap_name='gist_heat_r', chemical_mapping_mode=True)

def main():
    p = argparse.ArgumentParser()
    p.add_argument('inputfile')
    p.add_argument('construct_id')
    p.add_argument('--png', action='store_true',default=False)
    p.add_argument('--movie_mode', action='store_true')
    p.add_argument('--large_mode',action='store_true')

    args = p.parse_args()
    print(args)

    rdat_identifier=os.path.basename(args.inputfile).replace('.rdat','')
    construct_id = int(args.construct_id)
    draw_rdat_construct(args.inputfile, construct_id)

    if args.png:
        name = '%s_%d' % (rdat_identifier, construct_id)
        if 'INKSCAPEDIR' not in os.environ:
            print('Please set INKSCAPEDIR environmental variable with path to Inkscape app.')
            return
        inkscape = '%s/Contents/Resources/bin/inkscape' % os.environ['INKSCAPEDIR']
        if not os.path.isfile(inkscape):
            print('Inkscape not found. Please update INKSCAPEDIR environmental variable with path to Inkscape app.')
            return
        os.system('%s --export-png $(pwd)/%s.png --export-background-opacity 1 $(pwd)/%s.svg' % (inkscape, name, name))
        os.system('rm $(pwd)/%s.svg' % (name))

if __name__=='__main__':
    main()
