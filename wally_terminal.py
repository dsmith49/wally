from wally_json_control import Wally
import sys, termios, tty, os, time
from subprocess import call

def getch():
	fd = sys.stdin.fileno()
	old_settings = termios.tcgetattr(fd)
	try:
		tty.setraw(sys.stdin.fileno())
		ch = sys.stdin.read(1)
	finally:
		termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
	return ch

def display( status ):
	call('clear')
	print('DIRECTIONS: qwe        STOP: s')
	print('            a d        PENDOWN:[      PENUP:]   COMMAND_NAIVE:=    COMMAND_SMART:-')
	print('            zxc        EXIT: `        EXIT_AND_RELEASE_MOTORS:~')
	print('PEN1: 1     PEN2: 2    PEN3: 3')
	print('--------------------------------')
	print('POWER:', status['power'])
	print('           motor1      |      motor2')
	print('velocity: ',status['velocity'][0],'        ',status['velocity'][1])
	print('steps   : ',status['position_steps'][0],'  ',status['position_steps'][1])
	print('length  : ',"{:.2f}".format(status['position_meters'][0]),'  ',"{:.2f}".format(status['position_meters'][1]))
	print('Euclid  :',"{:.2f}".format(status['position_euclid'][0]),'  ',"{:.2f}".format(status['position_euclid'][1]))

def control_repl():
	exit = False
	wally = Wally()
	while not exit:
		status = wally.status()
		display( status )
		char = getch()
		command_dict = {}
		if (char == "1"): command_dict['command'] = 'PEN1'
		if (char == "2"): command_dict['command'] = 'PEN2'
		if (char == "3"): command_dict['command'] = 'PEN3'
		if (char == '['): command_dict['command'] = 'PENDOWN'
		if (char == ']'): command_dict['command'] = 'PENUP'
		if (char == "w"): command_dict['command'] = 'UP'
		if (char == "x"): command_dict['command'] = 'DOWN'
		if (char == "s"): command_dict['command'] = 'STOP'
		if (char == "q"): command_dict['command'] = 'UPLEFT'
		if (char == "e"): command_dict['command'] = 'UPRIGHT'
		if (char == "z"): command_dict['command'] = 'DOWNLEFT'
		if (char == "c"): command_dict['command'] = 'DOWNRIGHT'
		if (char == "a"): command_dict['command'] = 'LEFT'
		if (char == "d"): command_dict['command'] = 'RIGHT'
		if (char == "`"): command_dict['command'] = 'POWER'
		#if (char == " "): command_dict['command'] = 'PAUSE'
		if (char == "~"):
			command_dict['command'] = 'END'
			exit = True
		if (char == "p"): command_dict['command'] = 'CALIBRATE'
		if (char == '-'):
			command_dict['command'] = 'MOVE'
			response = input('SMART MOVE >> SPEED X_meters Y_meters>>')
			command_dict['speed'] = int(response.split(' ')[0])
			command_dict['relative_coords'] = [ float(response.split(' ')[1]), float(response.split(' ')[2]) ]
		if (char == 'o'):
			command_dict['command'] = 'DRAW'
			response = input('ENTER FILENAME>>')
			command_dict['filename'] = response
		wally.command( command_dict )

if __name__ == '__main__':
	control_repl()
