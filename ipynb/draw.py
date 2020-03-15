import matplotlib.pyplot as plt
import draw_rna.draw_rna.draw as d
from draw_rna.draw_rna.draw_utils import seq2col

def draw_struct(seq, secstruct, c=None, line=False, large_mode=False, cmap='viridis'):

    if c is not None:
        assert len(c) == len(seq)
        if isinstance(c[0], float):
            d.draw_rna(seq, secstruct, c, line=line, ext_color_file=True, cmap_name = cmap,
             large_mode = large_mode)
        else:
            d.draw_rna(seq, secstruct, c,  line=line, cmap_name=cmap, large_mode=large_mode)

    else:
        d.draw_rna(seq, secstruct, seq2col(seq), line=line, cmap_name = cmap,
         large_mode = large_mode)