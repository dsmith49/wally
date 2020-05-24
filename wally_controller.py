import json
import time
import motorlib
import config
from svgpathtools import svg2paths, Path, Line
from icm20948 import ICM20948
import sys
sys.path.append('/home/pi/wally/madgewick_py/')
from madgwickahrs import MadgwickAHRS
from quaternion import Quaternion
import numpy as np
import threading

class DrawObject(object):
	def __init__(self, filename='test', imagetype='PNG', width=0,height=0,pixels=[], paths=[], attributes={}):
		self.filename   = filename
		self.imagetype  = imagetype
		self.width      = width
		self.height     = height
		self.pixels     = pixels
		self.paths      = paths
		self.attributes = attributes

class IMU():
	def __init__(self):
		self.imu             = ICM20948()
		self.madgwick        = MadgwickAHRS(sampleperiod=0.01,quaternion=None,beta=0.1)
		self.updatethread    = threading.Thread( target=self.updater, daemon=True)
		self.updatethread.start()
	def update(self):
		x, y, z = self.imu.read_magnetometer_data()
		ax, ay, az, gx, gy, gz = self.imu.read_accelerometer_gyro_data()
		#self.madgwick.update( np.array([gx, gy, gz]), np.array([ax, ay, az]), np.array([x,y,z]) )
		self.madgwick.update_imu( np.array([gx, gy, gz]), np.array([ax, ay, az]) )
		print('updated', self.get() )
	def updater(self):
		while True:
			time.sleep(1)
			self.update()
	def get(self):
		return [self.madgwick.quaternion.to_euler_angles()]

class Wally(object):
	def __init__(self):
		self.config          = config.Config()
		self.config.loadJSON()
		self.motorlib        = motorlib.Motorlib( self.config )
		self.motors_on       = False
		self.ever_on         = False
		self.motors_velocity = [0,0]
		self.motors_position = [int(self.config.motor1_length / self.config.meters_per_step), int( self.config.motor2_length / self.config.meters_per_step) ]
		self.motors_last_velocity = [0,0]
		self.timestamp_1     = time.perf_counter()
		self.increment       = 500
		self.pwm             = None
		self.pendown         = False
		self.drawing         = False
		self.drawstatus      = [0,0]
		self.imu             = IMU()
		print('created IMU')

	def settings(self, settings=None):
		if (settings is None):
			return self.config.getJSON()	
		else:
			self.config.putJSON( settings )
			self.config.writeJSON()
			return None

	def status(self):
		statusdict = {
			'orientation' : self.imu.get(),
			'power'    : self.motors_on,
			'pendown'  : self.pendown,
			'velocity' : self.motors_velocity,
			'position_steps'    : self.motors_position,
			'position_meters'   : [self.motors_position[0] * self.config.meters_per_step, self.motors_position[1] * self.config.meters_per_step],
			'position_euclid'   : self.motorlib.hypoteni_to_euclid( self.motors_position )
		}
		print(self.imu.get())
		return statusdict #json.dumps( statusdict )

	def power(self, on=True, final=False):
		if (on and not self.motors_on):
			self.pwm = self.motorlib.configmotors( 0, first = not self.ever_on )
			self.motors_on = True
			self.ever_on   = True
		if (not on and self.motors_on):
			self.motorlib.close( self.pwm )
			self.motors_on = False
		if (final):
			self.motorlib.close( self.pwm, final=True)

	def pause(self):
		self.motorlib.stop()

	def pen_move(self, down=None):
		if (down is None):
			self.pendown = not self.pendown
		else:
			self.pendown = down
		if (not self.pendown):
			self.motorlib.setangle(self.pwm,0,self.config.pen_up_angle)
		else:
			self.motorlib.setangle(self.pwm,0,self.config.pen_down_angle)

	def pen_rotate(self, position):
		self.pen_move( down=False )
		if (position==0): self.motorlib.setangle(self.pwm,1,self.config.pen_1_angle)
		if (position==1): self.motorlib.setangle(self.pwm,1,self.config.pen_2_angle)
		if (position==2): self.motorlib.setangle(self.pwm,1,self.config.pen_3_angle)

	def calibrate(self):
		self.motors_velocity = [0,0]
		self.motors_position = [int( self.config.motor1_length / self.config.meters_per_step), int(self.config.motor2_length / self.config.meters_per_step) ]

	def drawSVG( self, data ):
		position = [0.0,0.0]
		self.drawing = True
		for num,path in enumerate(data.paths):
			print(path, num,'of',len(data.paths))
			self.drawstatus = [num,len(data.paths)]
			if (not self.drawing): return None
			x = path[0][0].real*self.config.meters_per_step * self.config.svg_pixel_size - position[0]
			y = path[0][0].imag*self.config.meters_per_step * self.config.svg_pixel_size - position[1]
			self.motors_position = self.motorlib.move( self.config.speed, [x,y], self.motors_position )
			position[0] += x
			position[1] += y
			self.pen_move()
			for num2,line in enumerate(path):
				if (not self.drawing): return None
				x = line[1].real * self.config.meters_per_step*self.config.svg_pixel_size - position[0]
				y = line[1].imag * self.config.meters_per_step*self.config.svg_pixel_size - position[1]
				self.motors_position = self.motorlib.move( self.config.speed, [x,y], self.motors_position )
				position[0] += x
				position[1] += y
			self.pen_move()
		self.drawing = False

	def loadfile(self, filename ):
		drawobject = None
		if (filename == 'test'):
			if ( len( sys.argv ) > 2): self.config.numlines = int( sys.argv[2] )
			width  = math.ceil( numlines**0.5 )
			height = math.ceil( numlines**0.5 )
			pixels = [[-1*(x*(256/numlines) - 255),255] for x in range(0, int( math.ceil( numlines**0.5 )**2) )]
			drawobject = DrawObject( imagetype='PNG', height=height, width=width,pixels=pixels)
		elif (filename.split('.')[1] == 'png'):
			print('loading file: ',filename )
			img     = Image.open( filename )
			width   = img.size[0]
			height  = img.size[1]
			pix_val = list(img.getdata())
			pixels = [[x,a] for (x,_,_,a) in pix_val]
			drawobject = DrawObject( filename=filename.split('.')[0], imagetype='PNG', height=height, width=width,pixels=pixels)
		elif (filename.split('.')[1] == 'svg'):
			print('loading file: ',filename )
			paths, attributes = svg2paths(filename)
			drawobject = DrawObject( imagetype='SVG', paths=paths, attributes=attributes)
		return drawobject

	def command(self, command_json):
		self.motors_last_velocity = self.motors_velocity.copy()
		command = command_json['command']
		print('command:',command)
		if (not self.motors_on and command != 'POWER'): return None
		if (command == 'UP'):
			self.motors_velocity[0] -= self.increment
			self.motors_velocity[1] -= self.increment
		elif (command == 'DOWN'):
			self.motors_velocity[0] += self.increment
			self.motors_velocity[1] += self.increment
		elif (command == "STOP"):
			self.motors_velocity[0] = 0
			self.motors_velocity[1] = 0
		elif (command == "UPLEFT"):
			self.motors_velocity[0] -= self.increment
		elif (command == "UPRIGHT"):
			self.motors_velocity[1] -= self.increment
		elif (command == "DOWNLEFT"):
			self.motors_velocity[1] += self.increment
		elif (command == "DOWNRIGHT"):
			self.motors_velocity[0] += self.increment
		elif (command == "LEFT"):
			self.motors_velocity[0] -= self.increment
			self.motors_velocity[1] += self.increment
		elif (command == "RIGHT"):
			self.motors_velocity[0] += self.increment
			self.motors_velocity[1] -= self.increment
		elif (command == "PEN1"): self.pen_rotate(0)
		elif (command == "PEN2"): self.pen_rotate(1)
		elif (command == "PEN3"): self.pen_rotate(2)
		elif (command == "PENDOWN"): self.pen_move(down=True)
		elif (command == "PENUP"): self.pen_move(down=False)
		elif (command == "POWER"): self.power(on=not self.motors_on)
		elif (command == "END"): self.power(on=False, final=True)
		elif (command == "CALIBRATE"): self.calibrate()
		elif (command in ["MOVE","DRAW"]):
			self.motors_velocity = [0,0]
		if (self.motors_on):
			self.motors_position = self.motorlib.update_motors( self.motors_last_velocity, self.motors_velocity, self.timestamp_1, self.motors_position)
			self.timestamp_1 = time.perf_counter()
		if (command == "MOVE"):
			self.motors_position = self.motorlib.move( command_json['speed'], command_json['relative_coords'], self.motors_position )
		if (command == "DRAW"):
			print('loading', command_json['filename'] )
			data = self.loadfile( command_json['filename'] )
			self.drawSVG( data )
		time.sleep(self.config.button_delay)

