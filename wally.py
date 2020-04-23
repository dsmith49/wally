#!/usr/bin/python
import sys
from PIL import Image
import motorlib
import math
import control

speed = 200
numlines = 8

class Gondola(object):
	boxsize  = (120,150)
	position = [0,0]
	speed    = 0
	pendown  = False
	crosshatch = False
	pwm      = None

	def __init__(self, pwm, speed):
		self.pwm = pwm
		self.speed = speed

	def tocoord(self, loc ): #puts gondola pen at upper left of loc box
		delta_x = (loc[0] - self.position[0]) * self. boxsize[0]
		delta_y = (loc[1] - self.position[1]) * self.boxsize[1]
		sign = 1
		movecommand_x = [sign * delta_x, - sign * delta_x]
		movecommand_y = [delta_y, delta_y]
		if (self.position[0] != loc[0]):
			motorlib.move( self.speed, movecommand_x )
		if (self.position[1] != loc[1]):
			motorlib.move( self.speed, movecommand_y )
		self.position = loc
		
	def togglepen(self):
		if self.pendown:
			control.pen_up(self.pwm)
		else:
			control.pen_down(self.pwm)
		self.pendown = not self.pendown

	def box(self, value ):
		lines = int( (255-value)/(256/numlines) )
		if (lines < 2): lines = 2
		print('drawing lines:', lines)
		self.togglepen()
		vertical_move = 0
		for y in range(0,lines):
			if (y % 2 == 0):
				motorlib.move( self.speed, [self.boxsize[0],-self.boxsize[0]] )
			else:
				motorlib.move( self.speed, [-self.boxsize[0],self.boxsize[0]] )
			if (y < (lines-1)):
				motorlib.move( self.speed, [int(self.boxsize[1]/(lines-1)),int(self.boxsize[1]/(lines-1))] )
				vertical_move += int(self.boxsize[1]/(lines-1))
		self.togglepen()
		if (lines % 2 == 0):
			motorlib.move( self.speed, [-vertical_move ,-vertical_move] )
		else:
			motorlib.move( self.speed, [-self.boxsize[0],self.boxsize[0]] )
			motorlib.move( self.speed, [-vertical_move ,-vertical_move ] )
		if (self.crosshatch):
			self.togglepen()
			horizontal_move = 0
			for x in range(0,lines):
				if (x % 2 == 0):
					motorlib.move( self.speed, [self.boxsize[1],self.boxsize[1]] )
				else:
					motorlib.move( self.speed, [-self.boxsize[1],-self.boxsize[1]] )
				if (x < (lines-1)):
					motorlib.move( self.speed, [int(self.boxsize[0]/(lines-1)),-1*int(self.boxsize[0]/(lines-1))] )
					horizontal_move += int(self.boxsize[0]/(lines-1))
			self.togglepen()
			if (lines % 2 == 0):
				motorlib.move( self.speed, [-horizontal_move,horizontal_move] )
			else:
				motorlib.move( self.speed, [-self.boxsize[1],-self.boxsize[1]] )
				motorlib.move( self.speed, [-horizontal_move,horizontal_move] )

	def crosshatchbox(self, value ):
		lines = int( (255-value)/(256/numlines) )
		if (lines < 2): lines = 2
		hlines = min( int(numlines/2), lines)
		vlines = max( 0, lines - int(numlines/2) )
		if (vlines == 1): vlines = 2
		print('drawing lines:', hlines,' ', vlines)
		self.togglepen()
		vertical_move = 0
		for y in range(0,hlines):
			if (y % 2 == 0):
				motorlib.move( self.speed, [self.boxsize[0],-self.boxsize[0]] )
			else:
				motorlib.move( self.speed, [-self.boxsize[0],self.boxsize[0]] )
			if (y < (hlines-1)):
				motorlib.move( self.speed, [int(self.boxsize[1]/(lines-1)),int(self.boxsize[1]/(lines-1))] )
				vertical_move += int(self.boxsize[1]/(lines-1))
		self.togglepen()
		if (hlines % 2 == 0):
			motorlib.move( self.speed, [-vertical_move ,-vertical_move] )
		else:
			motorlib.move( self.speed, [-self.boxsize[0],self.boxsize[0]] )
			motorlib.move( self.speed, [-vertical_move ,-vertical_move ] )
		if (self.crosshatch and vlines > 0):
			self.togglepen()
			horizontal_move = 0
			for x in range(0,vlines):
				if (x % 2 == 0):
					motorlib.move( self.speed, [self.boxsize[1],self.boxsize[1]] )
				else:
					motorlib.move( self.speed, [-self.boxsize[1],-self.boxsize[1]] )
				if (x < (vlines-1)):
					motorlib.move( self.speed, [int(self.boxsize[0]/(lines-1)),-1*int(self.boxsize[0]/(lines-1))] )
					horizontal_move += int(self.boxsize[0]/(lines-1))
			self.togglepen()
			if (vlines % 2 == 0):
				motorlib.move( self.speed, [-horizontal_move,horizontal_move] )
			else:
				motorlib.move( self.speed, [-self.boxsize[1],-self.boxsize[1]] )
				motorlib.move( self.speed, [-horizontal_move,horizontal_move] )

def loadfile():
	filename = sys.argv[1]
	width = 0
	height = 0
	pixels = 0
	if (filename == 'test'):
		if ( len( sys.argv ) > 1): numlines = int( sys.argv[2] )
		width  = math.ceil( numlines**0.5 )
		height = math.ceil( numlines**0.5 )
		pixels = [[-1*(x*(256/numlines) - 255),255] for x in range(0, int( math.ceil( numlines**0.5 )**2) )]
	else:
		print('loading file: ',filename )
		img = Image.open( filename )
		width = img.size[0]
		height = img.size[1]
		pix_val = list(img.getdata())
		print(pix_val)
		pixels = [[x,a] for (x,_,_,a) in pix_val]
	print(pixels)
	print(len(pixels))
	return (width, height, pixels)
	
def drawimage( gondola, data ):
	width, height, pixels = data
	print('height:',height,'width:',width,'len:',len(data))
	print(pixels)
	for y in range(0,height):
		for x in range(0,width):
			if (pixels[width*y + x][1] != 0):
				print('drawing box', str(x),',', str(y))
				gondola.tocoord( [x,y] )
				gondola.box( pixels[width*y + x][0] )


def main():
	if ( len(sys.argv) not in [1,2] ):
		print('USAGE') 
		print('python3 wally.py <image filename> <max number of lines per pixel>  #draws image with given resolution')
		print('OR')
		print('python3 wally.py test <max number of lines per pixel> # draws test grid with pixels ranging from 2 to max resolution')
		quit()
	control.control_repl()
	data = loadfile()
	pwm = motorlib.config( speed )
	gondola = Gondola( pwm, speed )
	drawimage( gondola, data )
	motorlib.close( pwm )

main()
