import draw_rna.svg as svg
import draw_rna.mpl as mpl
import draw_rna.render_rna as render_rna
import draw_rna.inv_utils as inv_utils
import numpy as np
import argparse
import re
from matplotlib import cm
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


NODE_R = 10
PRIMARY_SPACE = 20
PAIR_SPACE = 20

TEXT_SIZE = 50

RENDER_IN_LETTERS = True

COLORS = {#"r": [255, 0, 0],
          "r": [255, 102, 102],
          "g": [113, 188, 120],
          "b": [51, 153, 255],
          "p": [255, 210, 200],
          "k": [1, 0, 0],
          "y": [255, 211, 0],
          "c": [0, 255, 255],
          "m": [255, 0, 255],
          "w": [255, 255, 255],
          "e": [100, 100, 100],
          "f": [200, 200, 200],
          "o": [231, 115, 0],
          "i": [51, 204, 204],
          "h": [51, 153, 255],
          "u": [138, 43, 226]}
          #"h": [46, 184, 46]}

def draw_rna(sequence, secstruct, color_list, filename="secstruct", line=False,
    cmap_name='viridis', rotation=0, alpha=None,
    ext_color_file=False, chemical_mapping_mode=False, 
    large_mode=False, movie_mode=False, svg_mode=False, vmin=None, vmax=None, ax=None):

    if large_mode or movie_mode:
        CELL_PADDING = 100

        external_multiplier = 10000
        external_offset = np.pi + np.pi*rotation/180
    else:

        CELL_PADDING = 40
        external_multiplier = 1
        external_offset = 0 + np.pi*rotation/180
    
    r = render_rna.RNARenderer()
    pairmap = render_rna.get_pairmap_from_secstruct(secstruct)
    pairs = []
    for i in range(len(pairmap)):
        if pairmap[i] > i:
            pairs.append({"from":i, "to":pairmap[i], "p":1.0, "color":COLORS["e"]})

    r.setup_tree(secstruct, NODE_R, PRIMARY_SPACE, PAIR_SPACE, external_multiplier, external_offset)

    size = r.get_size()

    if large_mode or movie_mode:
        r.xarray_ = [x - r.xarray_[0] for x in r.xarray_]
        r.yarray_ = [y - r.yarray_[0] for y in r.yarray_]
        #print(np.min(r.xarray_), np.max(r.xarray_))
        #print(np.min(r.yarray_), np.max(r.yarray_))

        cell_size_x = np.max(r.xarray_) - np.min(r.xarray_) + CELL_PADDING * 2
        cell_size_y = np.max(r.yarray_) - np.min(r.yarray_) + CELL_PADDING * 2
        #print(cell_size_x, cell_size_y)

    else:
        cell_size_x = max(size) + CELL_PADDING * 2
        cell_size_y = max(size) + CELL_PADDING * 2

    # if colors are numeric, create color scale


    if ext_color_file:
        if vmin is None:
            vmin=np.min(color_list)
        if vmax is None:
            vmax=np.max(color_list)

        colormap = plt.get_cmap(cmap_name) 
        cNorm  = mcolors.Normalize(vmin=vmin, vmax=vmax)
        scalarMap = cm.ScalarMappable(norm=cNorm, cmap=colormap)
        colors = [scalarMap.to_rgba(val)[:-1] for val in color_list]
        colors = [[x*256 for x in y] for y in colors]

    else:
        if isinstance(color_list[0],str) and color_list[0].isalpha():
            colors = [COLORS[x] for x in list(color_list)]

        else: #if isinstance(color_list[0],float):
            print('Interpreting color string as integer values')
            colors = [float(x) for x in color_list]
            colormap = plt.get_cmap(cmap_name) 
            if vmin is None:
                vmin=np.min(colors)
            if vmax is None:
                vmax=np.max(colors)

            cNorm  = mcolors.Normalize(vmin=vmin, vmax=vmax)
            scalarMap = cm.ScalarMappable(norm=cNorm, cmap=colormap)
            colors = [scalarMap.to_rgba(val)[:-1] for val in colors]
            colors = [[x*256 for x in y] for y in colors]

    if svg_mode:
        # drawing object writes an svg file
        drawing_obj = svg.svg("%s.svg" % filename, cell_size_x, cell_size_y)
    else:
        if ax is None:
            fig, ax = plt.subplots(1,1,figsize=(cell_size_x/72, cell_size_y/72))
            drawing_obj = mpl.mpl(ax=ax)

        else:
            drawing_obj = mpl.mpl(ax=ax)

    if movie_mode or large_mode:
        r.draw(drawing_obj, CELL_PADDING, cell_size_y-CELL_PADDING,
         colors, pairs, sequence, RENDER_IN_LETTERS, external_offset, line, svg_mode, alpha)
    else:
        r.draw(drawing_obj, CELL_PADDING, CELL_PADDING, colors,
         pairs, sequence, RENDER_IN_LETTERS, external_offset, line, svg_mode, alpha )

    if not svg_mode:
        # apply matplotlib settings
        drawing_obj.clean_up()

def parse_colors(color_string):
    colorings = color_string.strip().split(",")
    colors = []
    for coloring in colorings:
        if "x" in coloring:
            [n, color] = coloring.split("x")
            colors += int(n) * [color]
        else:
            colors += [coloring]
    return colors[0]

def reorder_strands(order, seq, colors):
    breaks = [-1] + [m.start() for m in re.finditer("&", seq)] + [len(seq)]
    seq_segments = seq.split("&")
    color_segments = [colors[breaks[i]+1:breaks[i+1]] for i in range(len(breaks)-1)]

    seq = ""
    colors = []
    for strand in order:
        seq += seq_segments[strand-1] + "&"
        colors += color_segments[strand-1] + ["w"]
    return [seq[:-1], colors[:-1]]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="filename specifying sequences to fold", type=str)
    parser.add_argument("-f", "--fold", help="automatic folding", type=str)
    args = parser.parse_args()

    with open(args.filename) as f:
        n = int(f.readline())
        for i in range(n):
            seq = f.readline().strip()
            if args.fold == "nupack":
                result = inv_utils.nupack_fold(seq, 1e-7)
                secstruct = result[0]
                colors = parse_colors(f.readline())
                seq, colors = reorder_strands(result[2], seq, colors)
            elif args.fold == "vienna":
                secstruct = inv_utils.vienna_fold(seq)[0]
                colors = parse_colors(f.readline())
            else:
                secstruct = f.readline().strip()
                colors = parse_colors(f.readline())
            seq.replace("&", "")
            secstruct.replace("&", "")
            print(colors)
            draw_rna(seq, secstruct, colors, "%s_%d" % (args.filename, i))

if __name__ == "__main__":
    main()
