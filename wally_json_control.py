import json
import time
import motorlib
import config

class Wally(object):
	def __init__(self):
		self.motors_on = False
		self.ever_on   = False
		self.motors_velocity = [0,0]
		self.motors_position = [int(config.motor1_length / config.meters_per_step), int(config.motor2_length / config.meters_per_step) ]
		self.motors_last_velocity = [0,0]
		self.timestamp_1 = 0.0
		self.increment = 500
		self.pwm = None #motorlib.configmotors( 0 )
		self.pendown = False

	def status(self):
		statusdict = {
			'power'    : self.motors_on,
			'pendown'  : self.pendown,
			'velocity' : self.motors_velocity,
			'position_steps'    : self.motors_position,
			'position_meters'   : [self.motors_position[0] * config.meters_per_step, self.motors_position[1] * config.meters_per_step],
			'position_euclid'   : motorlib.hypoteni_to_euclid( self.motors_position )
		}
		return statusdict #json.dumps( statusdict )

	def power(self, on=True):
		print('begin',self.motors_on,on)
		if (on and not self.motors_on):
			self.pwm = motorlib.configmotors( 0, not self.ever_on )
			self.motors_on = True
			self.ever_on   = True
		if (not on and self.motors_on):
			motorlib.close( self.pwm )
			self.motors_on = False
		print('end',self.motors_on,on)

	def pause(self):
		motorlib.stop()

	def pen_move(self, down=None):
		if (down is None):
			self.pendown = not self.pendown
		else:
			sel.pendown = down
		if (not self.pendown):
			motorlib.setangle(self.pwm,0,config.pen_up_angle)
		else:
			motorlib.setangle(self.pwm,0,config.pen_down_angle)

	def pen_rotate(self, position):
		self.pen_move( down=False )
		if (position==0): motorlib.setangle(self.pwm,1,config.pen_1_angle)
		if (position==1): motorlib.setangle(self.pwm,1,config.pen_2_angle)
		if (position==2): motorlib.setangle(self.pwm,1,config.pen_3_angle)

	def calibrate(self):
		self.motors_velocity = [0,0]
		self.motors_position = [int(config.motor1_length / config.meters_per_step), int(config.motor2_length / config.meters_per_step) ]

	def command(self, command_json):
		self.motors_last_velocity = self.motors_velocity.copy()
		command = command_json['command']
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
		elif (command == "CALIBRATE"): self.calibrate()
		elif (command == "MOVE"):
			self.motors_velocity = [0,0]
		if (self.motors_on): self.motors_position = motorlib.update_motors( self.motors_last_velocity, self.motors_velocity, self.timestamp_1, self.motors_position)
		if (command == "MOVE"):
			self.motors_position = motorlib.move_smart2( command_json['speed'], command_json['relative_coords'], self.motors_position )
		timestamp_1 = time.perf_counter()
		time.sleep(config.button_delay)

