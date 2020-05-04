#!/usr/bin/python
import sys
from PIL import Image
import motorlib
import math
import control
import config

numlines = config.numlines

class Gondola(object):
	boxsize  = (120,150)
	position = [0,0]
	motors_position = [0,0]
	speed    = 0
	pendown  = False
	crosshatch = False
	pwm      = None

	def __init__(self, pwm, speed, motors_position):
		self.pwm = pwm
		self.speed = speed
		self.motors_position = motors_position

	def tocoord(self, loc ): #puts gondola pen at upper left of loc box
		delta_x = (loc[0] - self.position[0]) * config.boxsize[0] 
		delta_y = (loc[1] - self.position[1]) * config.boxsize[1]
		if (self.position[0] != loc[0]):
			self.motors_position = motorlib.move( self.speed, [delta_x,0], self.motors_position )
		if (self.position[1] != loc[1]):
			self.motors_position = motorlib.move( self.speed, [0,delta_y], self.motors_position )
		self.position = loc
		
	def togglepen(self):
		if self.pendown:
			control.pen_up(self.pwm)
		else:
			control.pen_down(self.pwm)
		self.pendown = not self.pendown

	def box(self, value ):
		lines = int( (255-value)/(256/numlines) )
		print('drawing lines:', lines)
		vertical_move = 0
		for y in range(0,lines):
			print('vertical move', y)
			if (y == 0):
				self.motors_position = motorlib.move( self.speed, [0,config.boxsize[1]/((lines)/2)], self.motors_position )
				vertical_move += config.boxsize[1]/((lines)/2)
			else:
				self.motors_position = motorlib.move( self.speed, [0,config.boxsize[1]/(lines)], self.motors_position )
				vertical_move += config.boxsize[1]/(lines)
			self.togglepen()
			print('horizontal line', y)
			if (y % 2 == 0):
				self.motors_position = motorlib.move( self.speed, [config.boxsize[0],0], self.motors_position)
			else:
				self.motors_position = motorlib.move( self.speed, [-config.boxsize[0],0], self.motors_position)
			self.togglepen()
		print('returning to top')
		self.motors_position = motorlib.move( self.speed, [0, -vertical_move] , self.motors_position )
		if (lines > 0 and lines % 2 != 0):
			print('returning to left')
			self.motors_position = motorlib.move( self.speed, [-config.boxsize[0],0], self.motors_position )

def loadfile():
	filename = sys.argv[1]
	width = 0
	height = 0
	pixels = 0
	if (filename == 'test'):
		if ( len( sys.argv ) > 2): config.numlines = int( sys.argv[2] )
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
	if ( len(sys.argv) not in [2,3] ):
		print('USAGE') 
		print('python3 wally.py <image filename> <max number of lines per pixel>  #draws image with given resolution')
		print('OR')
		print('python3 wally.py test <max number of lines per pixel> # draws test grid with pixels ranging from 2 to max resolution')
		print('EXAMPLE: python3 wally.py images/mario.png 8')
		quit()
	motors_position = control.control_repl()
	data    = loadfile()
	pwm     = motorlib.configmotors( config.speed )
	gondola = Gondola( pwm, config.speed, motors_position)
	drawimage( gondola, data )
	motorlib.close( pwm )

main()
