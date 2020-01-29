import render_rna_flip as render_rna
import svg
import inv_utils
import numpy as np
import argparse
import re
from matplotlib import cm
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

NODE_R = 10
PRIMARY_SPACE = 20
PAIR_SPACE = 20 #

CELL_PADDING = 40
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
          "o": [231, 115, 0],
          "i": [51, 204, 204],
          "h": [51, 153, 255],
          "u": [138, 43, 226]}
          #"h": [46, 184, 46]}

def draw_rna(sequence, secstruct, colors, filename="secstruct", line=False, cmap_name='gist_heat_r', ext_color_file=False, chemical_mapping_mode=False):
    r = render_rna.RNARenderer()

    pairmap = render_rna.get_pairmap_from_secstruct(secstruct)
    pairs = []
    for i in range(len(pairmap)):
        if pairmap[i] > i:
            pairs.append({"from":i, "to":pairmap[i], "p":1.0, "color":COLORS["e"]})
    r.setup_tree(secstruct, NODE_R, PRIMARY_SPACE, PAIR_SPACE)
    size = r.get_size()

    cell_size = max(size) + CELL_PADDING * 2

    # if colors are numeric, create color scale
    if ext_color_file:

        if chemical_mapping_mode:
            vmax = 3
        else:
            vmax = np.max(colors)

        colormap = plt.get_cmap(cmap_name) 
        cNorm  = mcolors.Normalize(vmin=0, vmax=3)
        scalarMap = cm.ScalarMappable(norm=cNorm, cmap=colormap)
        colors = [scalarMap.to_rgba(val)[:-1] for val in colors]
        colors = [[x*256 for x in y] for y in colors]

    else:
        # try:
        #     print('Interpreting color string as integer values')
        #     colors = [float(x) for x in colors.split()]
        #     colormap = plt.get_cmap(cmap_name) 
        #     cNorm  = mcolors.Normalize(vmin=0, vmax=3)
        #     scalarMap = cm.ScalarMappable(norm=cNorm, cmap=colormap)
        #     colors = [scalarMap.to_rgba(val)[:-1] for val in colors]
        #     colors = [[x*256 for x in y] for y in colors]
        # # otherwise, colors are indexes to COLORS dict
        # except:
        colors = [COLORS[x] for x in list(colors)]

    svgobj = svg.svg("%s.svg" % filename, cell_size, cell_size)
    r.draw(svgobj, CELL_PADDING, CELL_PADDING, colors, pairs, sequence, RENDER_IN_LETTERS, line)

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
