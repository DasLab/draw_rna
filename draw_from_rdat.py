from RDATKit import rdatkit
import draw_rna as d
import sys,os
import numpy as np

def draw_rdat_construct(rdat_file, construct_id):
    rdat_identifier=rdat_file.replace('.rdat','')
    
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

if __name__=='__main__':
    draw_rdat_construct(sys.argv[1], int(sys.argv[2]))
