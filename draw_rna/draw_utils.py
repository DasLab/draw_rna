def clamp(x): 
  return int(max(0, min(x, 255)))

def convert_color(color):
	"""Converts a color object (be it touple-like, or string to an SVG-readable color string)."""
	if type(color) == str:
		return color

	else:
		r,g,b = color
		return "#{0:02x}{1:02x}{2:02x}".format(clamp(r), clamp(g), clamp(b))

def seq2col(seq):
    color = {'A': 'y', 'U':'b', 'G':'r', 'C':'g', 'T': 'b', 'N': 'k', ' ': 'w'}
    col = []
    for c in seq:
        col.append(color[c])
    return col