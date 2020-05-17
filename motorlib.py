import piplates.MOTORplate as MOTOR
import RPi.GPIO as GPIO
import time
import config
import math

def configmotors( speed, first=False ):
	if (first):
		GPIO.setmode(GPIO.BCM)
		MOTOR.intEnable(0)                      #enable interrupts on Pi-Plate
		MOTOR.enablestepSTOPint(0,'A')          #set up to interrupt when motor a stops
		MOTOR.enablestepSTOPint(0,'B')          #set up to interrupt when motor a stops
	MOTOR.stepperCONFIG(0,'A', 'cw','H',speed,0)
	MOTOR.stepperCONFIG(0,'B', 'cw','H',speed,0)
	pwm = [None,None,time.perf_counter()]
	GPIO.setup(4, GPIO.OUT)
	GPIO.setup(5, GPIO.OUT)
	pwm[0]=GPIO.PWM(4, 50)
	pwm[0].start( 0 )
	pwm[1]=GPIO.PWM(5, 50)
	pwm[1].start( 0 )
	return pwm

def stop():
	MOTOR.stepperSTOP(0,'A')
	MOTOR.stepperSTOP(0,'B')

def off():
	MOTOR.stepperOFF(0,'A')
	MOTOR.stepperOFF(0,'B')

def close(pwm, final=False):
	pwm[0].stop()
	pwm[1].stop()
	stop()
	off()
	if (final): GPIO.cleanup()

def move_naive2( speed, command, motors_position ):
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
		time.sleep(0.05)                           #check every 100msec
		stat=MOTOR.getINTflag0(0)                 #read interrupt flags
		if (stat & (2 ** 4) ): 
			flag_b=0
		if (stat & (2 ** 5)) :
			flag_a=0
	return [motors_position[0] + command[0], motors_position[1] + command[1]]

def hypoteni_to_euclid( motors_position ):
	#herons formula
	#s = (motors_position[0]*config.meters_per_step + motors_position[1]*config.meters_per_step + config.x_total) / 2
	#a = (s * (s - motors_position[0]*config.meters_per_step) * ( s- motors_position[1]*config.meters_per_step ) * (s-config.x_total) )**0.5
	#y_from_top  = a / (0.5 * config.x_total)
	#x_from_left = ((motors_position[0]*config.meters_per_step)**2 - y_from_top**2)**0.5
	
	#height of trapezoid where a is long base, c is short base
	a = config.x_total
	b = motors_position[0] * config.meters_per_step
	c = 0.20
	d = motors_position[1] * config.meters_per_step
	y_from_top  = ((a+b-c+d) * (-a+b+c+d) * (a-b-c+d) * (a+b-c-d) / (4 * (a-c)**2))**0.5 + config.y_gondola
	x_from_left = ((motors_position[0]*config.meters_per_step)**2 - (y_from_top - config.y_gondola)**2 )**0.5 + config.x_gondola

	return [x_from_left, y_from_top]
	
def euclid_to_hypoteni( coordinate ):
	m1 = ( (coordinate[0] - config.x_gondola)**2 + (coordinate[1] - config.y_gondola)**2)**0.5 / config.meters_per_step
	m2 = ( ((config.x_total - coordinate[0]) - config.x_gondola)**2 + (coordinate[1] - config.y_gondola)**2)**0.5 / config.meters_per_step
	return [round(m1),round(m2)]

def motor_velocity_at_time( current_pos, end_pos, time, total_time):
	x_diff   = end_pos[0] - current_pos[0]
	y_diff   = end_pos[1] - current_pos[1]
	#dhdt_numerator   = x_diff * (x_diff * time + current_pos[0]) + y_diff * (y_diff * time + current_pos[1] )
	#dhdt_denomenator = ( (x_diff * time + current_pos[0])**2 + (y_diff * time + current_pos[1])**2 )**0.5
	if (not config.smartmove): current_pos = [config.x_total/2,config.x_total/2] 
	dhdt_numerator   = x_diff * (time * x_diff +current_pos[0] - config.x_gondola) + y_diff * (time * y_diff + current_pos[1] - config.y_gondola)
	dhdt_denomenator = ( (x_diff * time + current_pos[0] - config.x_gondola)**2 + (y_diff * time + current_pos[1] - config.y_gondola)**2 )**0.5
	return round( (dhdt_numerator/dhdt_denomenator) / (config.meters_per_step * total_time)) #returns velocity in steps per second

def move_smart( speed, command, motors_position ):
	
	current_position = hypoteni_to_euclid( motors_position )
	x_diff     		 = command[0]
	y_diff      	 = command[1]
	end_position     = [ current_position[0] + x_diff, current_position[1] + y_diff]
	distance    	 = ( x_diff**2 + y_diff**2 )**0.5
	total_time  	 = distance / (speed * config.meters_per_step)
	current_time 	 = 0

	current_position_mirror = [ config.x_total - current_position[0], current_position[1] ]
	end_position_mirror     = [ config.x_total - end_position[0], end_position[1] ]
	timestamp_1 = 0
	timestamp_2 = 0
	steps = [0,0]
	total_steps = [euclid_to_hypoteni( end_position )[0] - euclid_to_hypoteni( current_position )[0],euclid_to_hypoteni( end_position )[1] - euclid_to_hypoteni( current_position )[1]]

	while (abs(round(steps[0])) < abs(total_steps[0])) or (abs(round(steps[1])) < abs(total_steps[1])):
		motor1_velocity = motor_velocity_at_time( current_position, end_position, (current_time/total_time), total_time )
		motor2_velocity = motor_velocity_at_time( current_position_mirror, end_position_mirror, (current_time/total_time), total_time )
		if (current_time == 0):
			motor1_direction = 'ccw'
			motor2_direction = 'cw'
			if (motor1_velocity < 0): motor1_direction = 'cw'
			if (motor2_velocity < 0): motor2_direction = 'ccw'
			MOTOR.stepperCONFIG(0,'A', motor1_direction,'H', abs(motor1_velocity), 0 )
			MOTOR.stepperCONFIG(0,'B', motor2_direction,'H', abs(motor2_velocity), 0 )
			MOTOR.stepperJOG(0,'A')
			MOTOR.stepperJOG(0,'B')
			timestamp_1 = time.perf_counter()
		else:
			MOTOR.stepperRATE(0,'A', motor1_velocity)
			MOTOR.stepperRATE(0,'B', motor2_velocity)
		#time.sleep( 0.05 )
		timestamp_2  = time.perf_counter()
		current_time += (timestamp_2 - timestamp_1)
		steps[0] += ((timestamp_2 - timestamp_1) * motor1_velocity)
		steps[1] += ((timestamp_2 - timestamp_1) * motor2_velocity)
		timestamp_1  = timestamp_2
	MOTOR.stepperSTOP(0,'A')
	MOTOR.stepperSTOP(0,'B')
	return [motors_position[0] + round(steps[0]), motors_position[1] + round(steps[1])]

def move_smart2(speed, command, motors_position):
	start_position   = hypoteni_to_euclid( motors_position )
	x_diff     		 = command[0]
	y_diff      	 = command[1]
	end_position     = [ start_position[0] + x_diff, start_position[1] + y_diff]
	distance    	 = ( x_diff**2 + y_diff**2 )**0.5
	motors_position_begin = motors_position.copy()

	steps = math.ceil( distance / config.smart_step )
	current_command = [0,0]
	
	for step in range(0,steps):
		if (step < steps-1):
			current_command = [x_diff / steps, y_diff / steps]
		else:
			current_command = [x_diff - (x_diff/steps)*(steps-1), y_diff - (y_diff/steps)*(steps-1)]
		motors_position = move_smart_step( speed, current_command, motors_position )
	return motors_position

def move_smart_step( speed, command, motors_position ):

	current_position = hypoteni_to_euclid( motors_position )
	x_diff     		 = command[0]
	y_diff      	 = command[1]
	end_position     = [ current_position[0] + x_diff, current_position[1] + y_diff]
	motors_position_end = euclid_to_hypoteni( end_position )
	steps            = [motors_position_end[0] - motors_position[0], motors_position_end[1] - motors_position[1]]
	distance    	 = ( x_diff**2 + y_diff**2 )**0.5
	total_time  	 = distance / (speed * config.meters_per_step)

	current_position_mirror = [ config.x_total - current_position[0], current_position[1] ]
	end_position_mirror     = [ config.x_total - end_position[0], end_position[1] ]	
	motor1_velocity = motor_velocity_at_time( current_position, end_position, total_time/2, total_time )
	motor2_velocity = motor_velocity_at_time( current_position_mirror, end_position_mirror, total_time/2, total_time )

	print('in smart step with command', command, 'steps', steps,'and velocities', motor1_velocity, motor2_velocity)
	MOTOR.enablestepSTOPint(0,'A')          #set up to interrupt when motor a stops
	MOTOR.enablestepSTOPint(0,'B') 
	if (steps[0] == 0 and steps[1] == 0): return motors_position
	motor1_direction = 'ccw'
	motor2_direction = 'cw'
	if (motor1_velocity < 0): motor1_direction = 'cw'
	if (motor2_velocity < 0): motor2_direction = 'ccw'
	MOTOR.stepperCONFIG(0,'A', motor1_direction,'H',abs(motor1_velocity),0)
	MOTOR.stepperCONFIG(0,'B', motor2_direction,'H',abs(motor2_velocity),0)
	if (steps[0] != 0): MOTOR.stepperMOVE(0,'A', abs( steps[0] ))
	if (steps[1] != 0): MOTOR.stepperMOVE(0,'B', abs( steps[1] ))

	flag_a=1                                      #Initialize flag to true
	flag_b=1
	if (steps[0] == 0): flag_a = 0
	if (steps[1] == 0): flag_b = 0
	while(flag_a or flag_b):                      #start loop
		#time.sleep(0.05)                           #check every 100msec
		stat=MOTOR.getINTflag0(0)                 #read interrupt flags
		if (stat & (2 ** 4) ): 
			flag_b=0
		if (stat & (2 ** 5)) :
			flag_a=0
	return [motors_position[0] + steps[0], motors_position[1] + steps[1] ]

def move( speed, command, motors_position ):
	if config.smartmove:
		return move_smart2( speed, command, motors_position )
	else:
		return move_smart2( speed, command, motors_position )

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
	return [round(motors_position[0] + elapsed_time * motors_last_velocity[0]),round(motors_position[1] + elapsed_time * motors_last_velocity[1])]

def setangle(pwm, motorid, angle):
	#GPIO.output(4, True)
	timestamp = time.perf_counter()
	if (timestamp - pwm[2] < 0.5):
		time.sleep( timestamp - pwm[2] )
	pwm[motorid].ChangeDutyCycle( angle / 18 + 2.5 )
	pwm[2] = time.perf_counter()
	time.sleep(0.1)
	#GPIO.output(4, False)
	#pwm.ChangeDutyCycle(0)
