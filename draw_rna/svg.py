"""Methods for outputting SVG files."""

from draw_rna.draw_utils import *

class svg(object):
	def __init__(self, filename, w, h):
		# create the file
		self.__out = open(filename, 'w')

		# write the header
		self.__out.write("""
		<?xml version="1.0" encoding="utf-8"?>
		  <svg version="1.1" id="Layer_1"
		  x="0px" y="0px"
		  width="%spx" height="%spx"
		  viewBox="0 0 %s %s"
		  enable-background="new 0 0 247.44 234.492"
		  xml:space="preserve">""".replace('\t', '')[1:] % (w, h, w, h))
		self.__out.write('\n')

	def __del__(self):
		# write a footer
		self.__out.write('</svg>\n')
		self.__out.close()
		del self.__out

	def line(self, x1, y1, x2, y2, stroke, width=1, alpha=1):
		""""""
		# print 'Line (%s %s %s %s %s)' % (x1, y1, x2, y2, color)
		stroke = convert_color(stroke)
		self.__out.write('<line fill="none" stroke="%s" stroke-width="%dpx" x1="%s" y1="%s" x2="%s" y2="%s" x3="0.0" y3="0.0" alpha="%s"/>\n' %
			(stroke, width, x1, y1, x2, y2,alpha))

	def polygon(self, points, fill, stroke, opacity = 1.0):
		fill = convert_color(fill)
		stroke = convert_color(stroke)
		points = ' '.join('%s,%s' % (x,y) for (x,y) in points)
		self.__out.write('<polygon fill="%s" stroke="%s" points="%s" opacity="%f"/>\n' %
			(fill, stroke, points,opacity))

	def circle(self, x, y, radius, fill, stroke, alpha=1):
		fill = convert_color(fill)
		self.__out.write('<circle cx="%s" cy="%s" r="%s" fill="%s" stroke="%s" alpha="%s"/>\n' %
			(x, y, radius, fill, stroke,alpha))

	def text(self, x, y, size, fill, align, string,alpha=1):
		fill = convert_color(fill)
		self.__out.write(' <text x="%d" y="%d" font-family="sans_serif" font-size="%d" fill="%s" text-anchor="%s" alpha="%s">%s</text>' % (x,y,size,fill,align,alpha,string))
        ## rotated
		#self.__out.write(' <text x="%d" y="%d" font-family="sans_serif" font-size="%d" fill="%s" text-anchor="%s" transform="rotate(180 %d,%d)">%s</text>' % (x-10,y+10,size,fill,align,x,y,str))

