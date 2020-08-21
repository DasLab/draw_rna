import matplotlib.pyplot as plt
import draw_rna.draw as d
from draw_rna.draw_utils import seq2col

def draw_struct(seq, secstruct, c=None, line=False, large_mode=False,
 cmap='viridis', rotation=0, vmin=None, vmax=None, alpha=None, ax=None):
    '''
    Draw sequence with secondary structure.
    Inputs:
    c (string or array-like).  If string, characters must correspond to colors.
     If array-like obj, used as mapping for colormap (provided in cmap), or a string.
    line (bool): draw secstruct as line.
    large_mode: draw outer loop as straight line.
    rotation: rotate molecule (in degrees).
    '''

    if c is not None:
        assert len(c) == len(seq)
        if isinstance(c[0], float):
            d.draw_rna(seq, secstruct, c, line=line, ext_color_file=True, cmap_name = cmap, vmin=vmin, vmax=vmax,
             rotation=rotation, large_mode = large_mode, alpha=alpha, ax=ax)
        else:
            d.draw_rna(seq, secstruct, c,  line=line, cmap_name=cmap, large_mode=large_mode, vmin=vmin, vmax=vmax,
             rotation=rotation, alpha=alpha, ax=ax)

    else:
        d.draw_rna(seq, secstruct, seq2col(seq), line=line, cmap_name = cmap, vmin=vmin, vmax=vmax,
         large_mode = large_mode, rotation=rotation, alpha=alpha, ax=ax)

    if ax is None:
        plt.show()

    #return plt.gca()