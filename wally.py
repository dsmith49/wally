#!/usr/bin/python
import sys
from PIL import Image
import motorlib
import math
import control
import config

numlines = config.numlines

class Gondola(object):
	origin   = [0,0]
	position = [0,0]
	motors_position = [0,0]
	speed    = 0
	pendown  = False
	pwm      = None
	
	def __init__(self, pwm, speed, motors_position):
		self.pwm = pwm
		self.speed = speed
		self.motors_position = motors_position
		self.origin = motors_position.copy()

	def tocoord(self, loc ): #puts gondola pen at upper left of loc box
		if (config.smartmove):
			delta_x = (loc[0] - self.position[0]) * config.boxsize[0]
			delta_y = (loc[1] - self.position[1]) * config.boxsize[1]
			self.motors_position = motorlib.move( self.speed, [delta_x, delta_y], self.motors_position )
			self.motors_position = motorlib.move( self.speed, [0, 0], self.motors_position )
		else:
			delta_x = (loc[0] - self.position[0]) * config.boxsize_naive[0]
			delta_y = (loc[1] - self.position[1]) * config.boxsize_naive[1]
			self.motors_position = motorlib.move( self.speed, [delta_x + delta_y,-delta_x + delta_y], self.motors_position )
		self.position = loc
		
	def togglepen(self):
		if self.pendown:
			control.pen_up(self.pwm)
		else:
			control.pen_down(self.pwm)
		self.pendown = not self.pendown

	def box_naive(self, value ):
		lines     = int( (255-value)/(256/numlines) )
		vertical_lines   = 0
		horizontal_lines = lines
		if (config.crosshatch):
			horizontal_lines = math.ceil( lines / 2)
			vertical_lines   = lines - horizontal_lines
		print('drawing naive box w lines:', lines, 'at motors', [x*config.meters_per_step for x in self.motors_position], 'at euclid', motorlib.hypoteni_to_euclid( self.motors_position ))
		vertical_move = 0
		for y in range(0,horizontal_lines):
			if (y == 0):
				self.motors_position = motorlib.move( self.speed, [int((config.boxsize_naive[1]/horizontal_lines)/2),int((config.boxsize_naive[1]/horizontal_lines)/2)], self.motors_position )
				vertical_move += int((config.boxsize_naive[1]/horizontal_lines)/2)
			else:
				self.motors_position = motorlib.move( self.speed, [int((config.boxsize_naive[1]/horizontal_lines)),int((config.boxsize_naive[1]/horizontal_lines))], self.motors_position )
				vertical_move += int((config.boxsize_naive[1]/horizontal_lines))
			self.togglepen()
			if (y % 2 == 0):
				self.motors_position = motorlib.move( self.speed, [config.boxsize_naive[0],-config.boxsize_naive[0]], self.motors_position)
			else:
				self.motors_position = motorlib.move( self.speed, [-config.boxsize_naive[0],config.boxsize_naive[0]], self.motors_position)
			self.togglepen()
		self.motors_position = motorlib.move( self.speed, [-vertical_move, -vertical_move] , self.motors_position )
		if (horizontal_lines > 0 and horizontal_lines % 2 != 0):
			self.motors_position = motorlib.move( self.speed, [-config.boxsize_naive[0],config.boxsize_naive[0]], self.motors_position )
		if (config.crosshatch):
			horizontal_move = 0
			for y in range(0,vertical_lines):
				if (y == 0):
					self.motors_position = motorlib.move( self.speed, [int( (config.boxsize_naive[0]/vertical_lines)/2), -int( (config.boxsize_naive[0]/vertical_lines)/2)], self.motors_position )
					horizontal_move += int( (config.boxsize_naive[0]/vertical_lines)/2 )
				else:
					self.motors_position = motorlib.move( self.speed, [int(config.boxsize_naive[0]/vertical_lines),-int(config.boxsize_naive[0]/vertical_lines)], self.motors_position )
					horizontal_move += int( config.boxsize_naive[0]/(vertical_lines) )
				self.togglepen()
				if (y % 2 == 0):
					self.motors_position = motorlib.move( self.speed, [config.boxsize_naive[1],config.boxsize_naive[1]], self.motors_position)
				else:
					self.motors_position = motorlib.move( self.speed, [-config.boxsize_naive[1],-config.boxsize_naive[1]], self.motors_position)
				self.togglepen()
			self.motors_position = motorlib.move( self.speed, [-horizontal_move, horizontal_move] , self.motors_position )
			if (vertical_lines > 0 and vertical_lines % 2 != 0):
				self.motors_position = motorlib.move( self.speed, [-config.boxsize_naive[1],-config.boxsize_naive[1]], self.motors_position )

	def box(self, value ):
		lines     		 = int( (255-value)/(256/numlines) )
		vertical_lines   = 0
		horizontal_lines = lines
		if (config.crosshatch):
			horizontal_lines = math.ceil( lines / 2)
			vertical_lines   = lines - horizontal_lines
		print('drawing box w lines:', lines, 'at motors', [x*config.meters_per_step for x in self.motors_position], 'at euclid', motorlib.hypoteni_to_euclid( self.motors_position ))
		vertical_move = 0
		for y in range(0,horizontal_lines):
			if (y == 0):
				self.motors_position = motorlib.move( self.speed, [0,(config.boxsize[1]/horizontal_lines)/2], self.motors_position )
				vertical_move += (config.boxsize[1]/horizontal_lines)/2
			else:
				self.motors_position = motorlib.move( self.speed, [0,config.boxsize[1]/horizontal_lines], self.motors_position )
				vertical_move += config.boxsize[1]/(horizontal_lines)
			self.togglepen()
			if (y % 2 == 0):
				self.motors_position = motorlib.move( self.speed, [config.boxsize[0],0], self.motors_position)
			else:
				self.motors_position = motorlib.move( self.speed, [-config.boxsize[0],0], self.motors_position)
			self.togglepen()
		self.motors_position = motorlib.move( self.speed, [0, -vertical_move] , self.motors_position )
		if (horizontal_lines > 0 and horizontal_lines % 2 != 0):
			self.motors_position = motorlib.move( self.speed, [-config.boxsize[0],0], self.motors_position )
		if (config.crosshatch):
			horizontal_move = 0
			for y in range(0,vertical_lines):
				if (y == 0):
					self.motors_position = motorlib.move( self.speed, [(config.boxsize[0]/vertical_lines)/2,0], self.motors_position )
					horizontal_move += (config.boxsize[0]/vertical_lines)/2
				else:
					self.motors_position = motorlib.move( self.speed, [config.boxsize[0]/vertical_lines,0], self.motors_position )
					horizontal_move += config.boxsize[0]/(vertical_lines)
				self.togglepen()
				if (y % 2 == 0):
					self.motors_position = motorlib.move( self.speed, [0,config.boxsize[1]], self.motors_position)
				else:
					self.motors_position = motorlib.move( self.speed, [0,-config.boxsize[1]], self.motors_position)
				self.togglepen()
			self.motors_position = motorlib.move( self.speed, [-horizontal_move, 0] , self.motors_position )
			if (vertical_lines > 0 and vertical_lines % 2 != 0):
				self.motors_position = motorlib.move( self.speed, [0,-config.boxsize[1]], self.motors_position )

			

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
				if (config.smartmove):
					gondola.box( pixels[width*y + x][0] )
				else:
					gondola.box_naive( pixels[width*y + x][0] )


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
