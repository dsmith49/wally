import piplates.MOTORplate as MOTOR
import RPi.GPIO as GPIO
import time
import config

def configmotors( speed ):
	MOTOR.intEnable(0)                      #enable interrupts on Pi-Plate
	MOTOR.enablestepSTOPint(0,'A')          #set up to interrupt when motor a stops
	MOTOR.enablestepSTOPint(0,'B')          #set up to interrupt when motor a stops
	MOTOR.stepperCONFIG(0,'A', 'cw','H',speed,0)
	MOTOR.stepperCONFIG(0,'B', 'cw','H',speed,0)
	GPIO.setmode(GPIO.BCM)
	pwm = [None,None]
	GPIO.setup(4, GPIO.OUT)
	pwm[0]=GPIO.PWM(4, 50)
	pwm[0].start( config.pen_up_angle )
	GPIO.setup(5, GPIO.OUT)
	pwm[1]=GPIO.PWM(5, 50)
	pwm[1].start( config.pen_1_angle )
	return pwm

def stop():
	MOTOR.stepperSTOP(0,'A')
	MOTOR.stepperSTOP(0,'B')

def off():
	MOTOR.stepperOFF(0,'A')
	MOTOR.stepperOFF(0,'B')

def close(pwm):
	pwm[0].stop()
	pwm[1].stop()
	stop()
	off()
	GPIO.cleanup()

def euclid_to_hypoteni_naive( coordinate ):
	return [coordinate[0] + coordinate[1], -coordinate[0] + coordinate[1]]
def meters_to_steps( command ):
	return [ int(command[0] / config.meters_per_step), int(command[1] / config.meters_per_step) ]

def move_naive( speed, command_euclid, motors_position ):
	command = euclid_to_hypoteni_naive( meters_to_steps( command_euclid ) )
	MOTOR.enablestepSTOPint(0,'A')          #set up to interrupt when motor a stops
	MOTOR.enablestepSTOPint(0,'B') 
	if (command[0] == 0 and command[1] == 0): return motors_position
	motor1_direction = 'ccw'
	motor2_direction = 'cw'
	if (command[0] < 0): motor1_direction = 'cw'
	if (command[1] < 0): motor2_direction = 'ccw'
	MOTOR.stepperCONFIG(0,'A', motor1_direction,'H',speed,0)
	MOTOR.stepperCONFIG(0,'B', motor2_direction,'H',speed,0)
	if (command[0] != 0): MOTOR.stepperMOVE(0,'A', abs(command[0]))
	if (command[1] != 0): MOTOR.stepperMOVE(0,'B', abs(command[1]))

	flag_a=1                                      #Initialize flag to true
	flag_b=1
	if (command[0] == 0): flag_a = 0
	if (command[1] == 0): flag_b = 0
	while(flag_a or flag_b):                      #start loop
		time.sleep(0.1)                           #check every 100msec
		stat=MOTOR.getINTflag0(0)                 #read interrupt flags
		if (stat & (2 ** 4) ): 
			flag_b=0
		if (stat & (2 ** 5)) :
			flag_a=0
	return [motors_position[0] + command[0], motors_position[1] + command[1]]

def hypoteni_to_euclid( motors_position ):
	#herons formula
	s = (motors_position[0]*config.meters_per_step + motors_position[1]*config.meters_per_step + config.x_total) / 2
	a = (s * (s - motors_position[0]*config.meters_per_step) * ( s- motors_position[1]*config.meters_per_step ) * (s-config.x_total) )**0.5
	y_from_top  = a / (0.5 * config.x_total)
	x_from_left = ((motors_position[0]*config.meters_per_step)**2 - y_from_top**2)**0.5
	return [x_from_left, y_from_top]
	
def euclid_to_hypoteni( coordinate ):
	m1 = (coordinate[0]**2 + coordinate[1]**2)**0.5 / config.meters_per_step
	m2 = ((config.x_total - coordinate[0])**2 + coordinate[1]**2)**0.5 / config.meters_per_step
	return [m1,m2]

def motor_velocity_at_time( current_pos, end_pos, time, total_time ):
	x_diff   = end_pos[0] - current_pos[0]
	y_diff   = end_pos[1] - current_pos[1]
	dhdt_numerator   = x_diff * (x_diff * time + current_pos[0]) + y_diff * (y_diff * time + current_pos[1] )
	dhdt_denomenator = ( (x_diff * time + current_pos[0])**2 + (y_diff * time + current_pos[1])**2 )**0.5
	return int( (dhdt_numerator/dhdt_denomenator) / (config.meters_per_step * total_time)) #returns velocity in steps per second

def move( speed, command, motors_position ):
	return move_naive( speed, command, motors_position )

def update_motors(motors_last_velocity, motors_velocity, timestamp_1, motors_position):
	if (motors_last_velocity[0]==0):
		motor1_direction = 'ccw'
		if (motors_velocity[0] < 0): motor1_direction = 'cw'
		MOTOR.stepperCONFIG(0,'A',motor1_direction,'H',abs(motors_velocity[0]),0)
		MOTOR.stepperJOG(0,'A')
	if (motors_last_velocity[1]==0):
		motor2_direction = 'cw'
		if (motors_velocity[1] < 0): motor2_direction = 'ccw'
		MOTOR.stepperCONFIG(0,'B',motor2_direction,'H',abs(motors_velocity[1]),0)
		MOTOR.stepperJOG(0,'B')
	if (motors_velocity[0] == 0):
		MOTOR.stepperSTOP(0,'A')
	else:
		MOTOR.stepperRATE(0,'A', abs(motors_velocity[0]))
	if (motors_velocity[1] == 0):
		MOTOR.stepperSTOP(0,'B')
	else:
		MOTOR.stepperRATE(0,'B', abs(motors_velocity[1]))
	timestamp_2 = time.perf_counter()
	elapsed_time = timestamp_2 - timestamp_1
	return [motors_position[0] + elapsed_time * motors_last_velocity[0],motors_position[1] + elapsed_time * motors_last_velocity[1]]

def setangle(pwm, motorid, angle):
	#GPIO.output(4, True)
	pwm[motorid].ChangeDutyCycle( angle / 18 + 2.5 )
	time.sleep(0.5)
	#GPIO.output(4, False)
	#pwm.ChangeDutyCycle(0)
