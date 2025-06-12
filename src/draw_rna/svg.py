"""Methods for outputting SVG files."""
from io import BytesIO
from base64 import b64encode
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
from draw_rna.draw_utils import *

class svg(object):
	def __init__(self, filename, w, h, padding):
		self.w = w
		self.h = h
		self.padding = padding

		self.miny = 0
		self.maxy = h

		self.__out = open(filename, 'w')

		self.elements = []

	def __del__(self):
		# write the header
		self.__out.write("""
		<?xml version="1.0" encoding="utf-8"?>
		  <svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg"
		  x="0px" y="0px"
		  width="%spx" height="%spx"
		  viewBox="%s %s %s %s"
		  enable-background="new 0 0 247.44 234.492"
		  xml:space="preserve">""".replace('\t', '')[1:] % (self.w, self.maxy - self.miny, 0, self.miny, self.w, self.maxy - self.miny))
		self.__out.write('\n')

		for element in self.elements:
			self.__out.write(element)
		
		# write a footer
		self.__out.write('</svg>\n')

		self.__out.close()
		del self.__out

	def line(self, x1, y1, x2, y2, stroke, width=1, alpha=1):
		""""""
		# print 'Line (%s %s %s %s %s)' % (x1, y1, x2, y2, color)
		stroke = convert_color(stroke)
		self.elements.append('<line fill="none" stroke="%s" stroke-width="%dpx" x1="%s" y1="%s" x2="%s" y2="%s" x3="0.0" y3="0.0" alpha="%s"/>\n' %
			(stroke, width, x1, y1, x2, y2,alpha))

	def polygon(self, points, fill, stroke, opacity = 1.0):
		fill = convert_color(fill)
		stroke = convert_color(stroke)
		points = ' '.join('%s,%s' % (x,y) for (x,y) in points)
		self.elements.append('<polygon fill="%s" stroke="%s" points="%s" opacity="%f"/>\n' %
			(fill, stroke, points,opacity))

	def circle(self, x, y, radius, fill, stroke, alpha=1):
		fill = convert_color(fill)
		self.elements.append('<circle cx="%s" cy="%s" r="%s" fill="%s" stroke="%s" alpha="%s"/>\n' %
			(x, y, radius, fill, stroke,alpha))

	def text(self, x, y, size, fill, align, string,alpha=1,align_y='center'):
		if y < self.miny:
			self.miny = y - self.padding

		fill = convert_color(fill)
		if align_y == 'center':
			dominant_baseline = 'middle'
		elif align_y == 'top':
			dominant_baseline = 'hanging'
		self.elements.append(' <text x="%d" y="%d" font-family="sans_serif" font-size="%d" fill="%s" text-anchor="%s" dominant-baseline="%s" alpha="%s">%s</text>' % (x,y,size,fill,'middle',dominant_baseline,alpha,string))
        ## rotated
		#self.elements.append(' <text x="%d" y="%d" font-family="sans_serif" font-size="%d" fill="%s" text-anchor="%s" transform="rotate(180 %d,%d)">%s</text>' % (x-10,y+10,size,fill,align,x,y,str))

	def colorbar(self, cmap_name, fraction, aspect, label=None, **kwargs):
		h = self.h * fraction
		w = h * aspect

		fig, ax = plt.subplots(figsize=(w / 72, h / 72))
		fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
		fig.colorbar(ScalarMappable(norm=Normalize(0, 1), cmap=cmap_name), cax=ax, **kwargs)
		
		out = BytesIO()
		fig.savefig(out, bbox_inches='tight', pad_inches=0, transparent=True, dpi=300)
		out.seek(0)

		bbox = fig.get_tightbbox()
		final_width = bbox.width * 72
		final_height = bbox.height * 72

		x = (self.w  - final_width) / 2
		y = self.h
		self.elements.append('<image href="data:image/png;base64,%s" x="%s" y="%s" width="%s" height="%s" />' % (b64encode(out.read()).decode(), x, y, final_width, final_height))

		if label:
			self.text(self.w/2, y + final_height + final_height/16, final_height // 2, "#000000", 'center', label, align_y='top')
			self.maxy = y + final_height + final_height/16 + final_height//2 + self.padding
		else:
			self.maxy = y + final_height + self.padding
