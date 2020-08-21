import matplotlib.pyplot as plt
from draw_rna.draw_utils import * 

class mpl(object):
	def __init__(self, ax, dpi=72):
		# create the file
		#self.dpi = dpi
		#plt.figure(figsize=(w/self.dpi,h/self.dpi), dpi=self.dpi)
		self.ax=ax
		plt.sca(self.ax)

	def line(self, x1, y1, x2, y2, stroke, width=1, alpha=1):
		""""""
		# print 'Line (%s %s %s %s %s)' % (x1, y1, x2, y2, color)
		stroke = convert_color(stroke)

		plt.plot([x1,x2], [y1,y2], linewidth=width, c=stroke, zorder=0, alpha=alpha)

	def circle(self, x, y, radius, fill, stroke, alpha=1):
		fill = convert_color(fill)
		plt.scatter(x,y,s=1,zorder=0,alpha=alpha)
		circ = plt.Circle((x,y),radius=radius, alpha=alpha, color=fill, zorder=1, linewidth=0)
		self.ax.add_artist(circ)
	
	def text(self, x, y, size, fill, align, string, alpha=1):
		fill = convert_color(fill)
		plt.text(x,y,string, fontsize=size, color=fill, zorder=2, horizontalalignment='center', verticalalignment='center', alpha=alpha)
        ## rotated 
		#self.__out.write(' <text x="%d" y="%d" font-family="sans_serif" font-size="%d" fill="%s" text-anchor="%s" transform="rotate(180 %d,%d)">%s</text>' % (x-10,y+10,size,fill,align,x,y,str))
	
	def clean_up(self):
		self.ax.set_aspect('equal')
		plt.axis('off')
		l, r = plt.xlim()
		plt.xlim(l-20,r+20)
		b,t = plt.ylim()
		plt.ylim(b-20,t+20)
