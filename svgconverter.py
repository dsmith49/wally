import linedraw
import sys
from svgpathtools import svg2paths, wsvg, Path, Line

import sys
import os
from PIL import Image
from math import ceil
import config

#xmin=0
#xmax=0
#ymin=0
#ymax=0
#paths, attributes = svg2paths(sys.argv[1])
#for path in paths:
#	for line in path:
#		print(line)
#		xmin = min(line[0].real,line[1].real,xmin)
#		ymin = min(line[0].imag,line[1].imag,ymin)
#		xmax = max(line[0].real,line[1].real,xmax)
#		ymax = max(line[0].imag,line[1].imag,ymax)

#print('x max and min', xmax, xmin)
#print('y max and min',ymax,ymin)
#print('width =',xmax + abs(xmin))
#print('height = ',ymax + abs(ymin))

#newpaths = []
#for path in paths:
#	newpath = Path()
#	for line in path:
#		newline = Line(complex(line[0].real + abs(xmin), line[0].imag + abs(ymin)), complex(line[1].real + abs(xmin), line[1].imag + abs(ymin)))
#		newpath.append(newline)
#	newpaths.append(newpath)

#wsvg(newpaths, filename='output.svg')

class DrawObject(object):
	def __init__(self, filename='test', imagetype='PNG', width=0,height=0,pixels=[], paths=[], attributes={}):
		self.filename   = filename
		self.imagetype  = imagetype
		self.width      = width
		self.height     = height
		self.pixels     = pixels
		self.paths      = paths
		self.attributes = attributes

def svgbox( pixelid, crosshatch, value, numlines ):
	lines     		 = int( (255-value)/(256/numlines) )
	vertical_lines   = 0
	horizontal_lines = lines
	if (crosshatch):
		horizontal_lines = ceil( lines / 2)
		vertical_lines   = lines - horizontal_lines
	paths         = []
	move          = []
	origin        = [pixelid[0]*(config.boxsize[0]/config.meters_per_step), pixelid[1]*(config.boxsize[1]/config.meters_per_step) ]
	current_loc   = origin.copy()
	for y in range(0,horizontal_lines):
		if (y == 0):
			move = [0,((config.boxsize[1]/config.meters_per_step)/horizontal_lines)/2]
			current_loc = [ current_loc[0] + move[0], current_loc[1] + move[1] ]
		else:
			move = [0,((config.boxsize[1]/config.meters_per_step)/horizontal_lines)]
			current_loc = [ current_loc[0] + move[0], current_loc[1] + move[1] ]
		if (y % 2 == 0):
			move = [config.boxsize[0]/config.meters_per_step,0]
		else:
			move = [-config.boxsize[0]/config.meters_per_step,0]
		paths.append( Path( Line( complex(current_loc[0], current_loc[1]), complex(current_loc[0] + move[0], current_loc[1] + move[1] ) ) ) )
		current_loc = [ current_loc[0] + move[0], current_loc[1] + move[1] ]
	current_loc = origin.copy()
	if (crosshatch):
		for y in range(0,vertical_lines):
			if (y == 0):
				move = [((config.boxsize[0]/config.meters_per_step)/vertical_lines)/2,0]
				current_loc = [ current_loc[0] + move[0], current_loc[1] + move[1] ]
			else:
				move = [(config.boxsize[0]/config.meters_per_step)/vertical_lines,0]
				current_loc = [ current_loc[0] + move[0], current_loc[1] + move[1] ]
			if (y % 2 == 0):
				move = [0,config.boxsize[1]/config.meters_per_step]
			else:
				move = [0,-config.boxsize[1]/config.meters_per_step]
			paths.append( Path( Line( complex(current_loc[0], current_loc[1]), complex(current_loc[0] + move[0], current_loc[1] + move[1] ) ) ) )
			current_loc = [ current_loc[0] + move[0], current_loc[1] + move[1] ]
		current_loc = origin.copy()			
	return paths

def loadfile( filename ):
	drawobject = None
	if (filename == 'test'):
		if ( len( sys.argv ) > 3): config.numlines = int( sys.argv[3] )
		width  = ceil( numlines**0.5 )
		height = ceil( numlines**0.5 )
		pixels = [[-1*(x*(256/numlines) - 255),255] for x in range(0, int( ceil( numlines**0.5 )**2) )]
		drawobject = DrawObject( imagetype='PNG', height=height, width=width,pixels=pixels)
	elif (filename.split('.')[1] == 'png'):
		print('loading file: ',filename )
		img     = Image.open( filename )
		width   = img.size[0]
		height  = img.size[1]
		pix_val = list(img.getdata())
		pixels = [[x,a] for (x,_,_,a) in pix_val]
		drawobject = DrawObject( filename=filename.split('.')[0], imagetype='PNG', height=height, width=width,pixels=pixels)
	else:
		print('file must be PNG')
		exit()
	return drawobject

def pngtosvg( data, filename, crosshatch, numlines ):
	newpaths = []
	for y in range(0,data.height):
		for x in range(0,data.width):
			if (data.pixels[data.width*y + x][1] != 0):
				newpaths = newpaths + svgbox( [x,y], crosshatch, data.pixels[data.width*y + x][0], numlines)
	wsvg( newpaths, filename=filename.split('.')[0] + '.svg')

def main():
	if ( len(sys.argv) not in [5] ):
		print('USAGE: python3 svgconverter.py <filename> <CONTOUR|PIXEL> <hatching INT> <contour INT>')
		print('if mode is CONTOUR, hatching in [0,32], contour in [0,4]')
		print('if mode is PIXEL, hatching > 0 sets crosshatch to True, else False, contour is numlines per pixel, in [0,32]')
		exit()
	filename     = sys.argv[1]
	convert_type = sys.argv[2]
	hatching     = int(sys.argv[3])
	contour      = int(sys.argv[4])
	print( os.path.split(filename) )
	if (convert_type == 'CONTOUR'):
		linedraw.vectorise(filename.split('.')[0], draw_hatch=hatching,draw_contours=contour)
	if (convert_type == 'PIXEL'):
		data  = loadfile( filename )
		pngtosvg( data, filename, hatching, contour)

main()
