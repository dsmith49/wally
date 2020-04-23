#!/usr/bin/python
import sys, termios, tty, os, time
from subprocess import call
import motorlib

# constants to be set before use 
x_total = 10
y_total = 5
button_delay = 0.05

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
	call('clear')
	print('       motor1      |      motor2')
	print('velocity: ',motors_velocity[0],'        ',motors_velocity[1])
	print('location: ',"{:.2f}".format(motors_position[0]),'  ',"{:.2f}".format(motors_position[1]))

def update_distance(time_stamp_1, motors_last_velocity, motors_position):
	time_stamp_2 = time.perf_counter()
	elapsed_time = time_stamp_2 - time_stamp_1
	new_location = [motors_position[0] + elapsed_time * motors_last_velocity[0],motors_position[1] + elapsed_time * motors_last_velocity[1]]
	return new_location

def pen_up(pwm):
	motorlib.setangle(pwm,45)

def pen_down(pwm):
	motorlib.setangle(pwm,30)

def control_repl():
	exit = False
	motors_velocity = [0,0]
	motors_position = [0,0]
	motors_last_velocity = [0,0]
	timestamp_1 = 0.0
	increment = 500
	pwm = motorlib.config( 0 )
	while not exit:
		display_motors( motors_velocity, motors_position)
		char = getch()
		motors_last_velocity = motors_velocity.copy()
		if (char == "w"):
			motors_velocity[0] += increment
			motors_velocity[1] += increment
		if (char == "x"):
			motors_velocity[0] -= increment
			motors_velocity[1] -= increment
		if (char == "s"):
			motors_velocity[0] = 0
			motors_velocity[1] = 0
		if (char == "q"):
			motors_velocity[0] += increment
		if (char == "e"):
			motors_velocity[1] += increment
		if (char == "z"):
			motors_velocity[1] -= increment
		if (char == "c"):
			motors_velocity[0] -= increment
		if (char == "a"):
			motors_velocity[0] += increment
			motors_velocity[1] -= increment
		if (char == "d"):
			motors_velocity[0] -= increment
			motors_velocity[1] += increment
		if (char == "`"): exit = True
		if (char == "p"):
			motors_velocity = [0,0]
			motors_position = [0,0]
		if (char == '['): pen_down(pwm)
		if (char == ']'): pen_up(pwm)
		motorlib.update_motors( motors_last_velocity, motors_velocity)
		motors_position = update_distance(timestamp_1, motors_last_velocity,motors_position)
		timestamp_1 = time.perf_counter()
		time.sleep(button_delay)
	motorlib.stop()

if __name__ == '__main__':
	control_repl()
