import render_rna_flip as render_rna
import svg
import inv_utils
import argparse
import re
from matplotlib import cm

NODE_R = 10
PRIMARY_SPACE = 20
PAIR_SPACE = 23

CELL_PADDING = 40
TEXT_SIZE = 50

RENDER_IN_LETTERS = True

COLORS = {#"r": [255, 0, 0],
          "r": [255, 102, 102],
          "g": [113, 188, 120],
          "b": [51, 153, 255],
          #"b": [0, 153, 255],
          "k": [1, 0, 0],
          "y": [255, 211, 0],
          "c": [0, 255, 255],
          "m": [255, 0, 255],
          "w": [255, 255, 255],
          "e": [100, 100, 100],
          "o": [231, 115, 0],
          "i": [51, 204, 204],
          "h": [51, 153, 255]}
          #"i": [0, 204, 153],
          #"h": [46, 184, 46]}

def draw_rna(sequence, secstruct, colors, filename="secstruct", line=False):
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
    try:
        colors = [float(x) for x in colors.split()]
        gist_earth = cm.get_cmap('gist_earth_r')
        min_ = min(colors)
        range_ = max(colors) - min_
        colors = [gist_earth((x - min_)/range_)[:-1] for x in colors]
        colors = [[c * 256 for c in color] for color in colors]
    # otherwise, colors are indexes to COLORS dict
    except:
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
    return colors

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
            draw_rna(seq, secstruct, colors, "%s_%d" % (args.filename, i))

if __name__ == "__main__":
    main()
