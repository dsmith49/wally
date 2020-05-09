#!/usr/bin/python
import sys, termios, tty, os, time
from subprocess import call
import motorlib
import config

def getch():
	fd = sys.stdin.fileno()
	old_settings = termios.tcgetattr(fd)
	try:
		tty.setraw(sys.stdin.fileno())
		ch = sys.stdin.read(1)
	finally:
		termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
	return ch

def display_motors(motors_velocity, motors_position ):
	euclid_position = motorlib.hypoteni_to_euclid( motors_position )
	#call('clear')
	print('DIRECTIONS: qwe        STOP: s')
	print('            a d        PENDOWN:[      PENUP:]   COMMAND:=')
	print('            zxc        EXIT: `        EXIT_AND_RELEASE_MOTORS:~')
	print('PEN1: 1     PEN2: 2    PEN3: 3')
	print('--------------------------------')
	print('       motor1      |      motor2')
	print('velocity: ',motors_velocity[0],'        ',motors_velocity[1])
	print('steps: ',motors_position[0],'  ',motors_position[1])
	print('length: ',"{:.2f}".format(motors_position[0] * config.meters_per_step),'  ',"{:.2f}".format(motors_position[1] * config.meters_per_step))
	print('Euclid:',"{:.2f}".format(euclid_position[0]),' ',"{:.2f}".format(euclid_position[1]))

def pen_up(pwm):
	motorlib.setangle(pwm,0,config.pen_up_angle)

def pen_down(pwm):
	motorlib.setangle(pwm,0,config.pen_down_angle)

def pen_rotate(pwm, position):
	pen_up( pwm )
	if (position==0): motorlib.setangle(pwm,1,config.pen_1_angle)
	if (position==1): motorlib.setangle(pwm,1,config.pen_2_angle)
	if (position==2): motorlib.setangle(pwm,1,config.pen_3_angle)

def control_repl():
	exit = False
	motors = True
	motors_velocity = [0,0]
	motors_position = [int(config.motor1_length / config.meters_per_step), int(config.motor2_length / config.meters_per_step) ]
	motors_last_velocity = [0,0]
	timestamp_1 = 0.0
	increment = 500
	pwm = motorlib.configmotors( 0 )
	while not exit:
		display_motors( motors_velocity, motors_position)
		char = getch()
		motors_last_velocity = motors_velocity.copy()
		if (char == "1"): pen_rotate(pwm,0)
		if (char == "2"): pen_rotate(pwm,1)
		if (char == "3"): pen_rotate(pwm,2)
		if (char == "w"):
			motors_velocity[0] -= increment
			motors_velocity[1] -= increment
		if (char == "x"):
			motors_velocity[0] += increment
			motors_velocity[1] += increment
		if (char == "s"):
			motors_velocity[0] = 0
			motors_velocity[1] = 0
		if (char == "q"):
			motors_velocity[0] -= increment
		if (char == "e"):
			motors_velocity[1] -= increment
		if (char == "z"):
			motors_velocity[1] += increment
		if (char == "c"):
			motors_velocity[0] += increment
		if (char == "a"):
			motors_velocity[0] -= increment
			motors_velocity[1] += increment
		if (char == "d"):
			motors_velocity[0] += increment
			motors_velocity[1] -= increment
		if (char == "`"):
			exit = True
		if (char == "~"): 
			motors = False
			exit = True
		if (char == "p"):
			motors_velocity = [0,0]
			motors_position = [int(config.motor1_length / config.meters_per_step), int(config.motor2_length / config.meters_per_ste) ]
		if (char == '['): pen_down(pwm)
		if (char == ']'): pen_up(pwm)
		if (char == '='):
			motors_velocity = [0,0]
			motors_position = motorlib.update_motors( motors_last_velocity, motors_velocity, timestamp_1, motors_position)
			response = input('NAIVE MOVE >> SPEED M1_steps M2_steps>>')
			if (len(response.split(' ')) == 3):
				speed = int( response.split(' ')[0] )
				command = [ int(x) for x in response.split(' ')[1:] ]
			else:
				command = [ int(x) for x in response.split(' ') ]
			motors_position = motorlib.move_naive2( speed, command, motors_position )
		if (char == '-'):
			motors_velocity = [0,0]
			motors_position = motorlib.update_motors( motors_last_velocity, motors_velocity, timestamp_1, motors_position)
			response = input('SMART MOVE >> SPEED X_meters Y_meters>>')
			if (len(response.split(' ')) == 3):
				speed = int( response.split(' ')[0] )
				command = [ float(x) for x in response.split(' ')[1:] ]
			else:
				command = [ float(x) for x in response.split(' ') ]
			motors_position = motorlib.move_smart2( speed, command, motors_position )

		motors_position = motorlib.update_motors( motors_last_velocity, motors_velocity, timestamp_1, motors_position)
		timestamp_1 = time.perf_counter()
		time.sleep(config.button_delay)
	motorlib.stop()
	if (not motors): motorlib.off()
	return motors_position

if __name__ == '__main__':
	control_repl()
