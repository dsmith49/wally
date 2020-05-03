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
	GPIO.setup(4, GPIO.OUT)
	pwm=GPIO.PWM(4, 50)
	pwm.start(4.444)
	return pwm

def stop():
	MOTOR.stepperSTOP(0,'A')
	MOTOR.stepperSTOP(0,'B')

def off():
	MOTOR.stepperOFF(0,'A')
	MOTOR.stepperOFF(0,'B')

def close(pwm):
	pwm.stop()
	stop()
	off()
	GPIO.cleanup()

def move_naive( speed, command, motors_position ):
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

def motor_velocity_at_time( current_pos, end_pos, time ):
	x_diff   = end_pos[0] - current_pos[0]
	y_diff   = end_pos[1] - current_pos[1]
	velocity = x_diff**2 * time + x_diff * current_pos[0] + y_diff**2 * time + y_diff * current_pos[1]
	return (velocity / config.meters_per_step) #returns velocity in steps per second

def move_smart( speed, command, motors_position ):
	
	#herons formula
	s = (motors_position[0]*config.meters_per_step + motors_position[1]*config.meters_per_step + config.x_total) / 2
	a = (s * (s - motors_position[0]*config.meters_per_step) * ( motors_position[1]*config.meters_per_step ) * config.x_total)**0.5
	y_from_top  = a / (0.5 * config.x_total)
	x_from_left = ((motors_position[0]*config.meters_per_step)**2 - y_from_top**2)**0.5

	x_diff     		 = command[0] * config.meters_per_step
	y_diff      	 = command[1] * config.meters_per_step
	current_position = [x_from_left, y_from_top]
	end_position     = [x_from_left + x_diff, y_from_top + y_diff]
	distance    	 = ( x_diff**2 + y_diff**2 )**0.5
	total_time  	 = distance / speed
	current_time 	 = 0
	print('current position', current_position)
	print('end position', end_position)

	current_position_mirror = [ config.x_total - current_position[0], current_position[1] ]
	end_position_mirror     = [ config.x_total - end_position[0], end_position[1] ]

	while (current_time < total_time):
		motor1_velocity = motor_velocity_at_time( current_position, end_position, current_time )
		motor2_velocity = motor_velocity_at_time( current_position_mirror, end_position_mirror, current_time )
		print('velocities', motor1_velocity, motor2_velocity)
		if (current_time == 0):
			motor1_direction = 'ccw'
			motor2_direction = 'cw'
			if (motor1_velocity < 0): motor1_direction = 'cw'
			if (motor2_velocity < 0): motor2_direction = 'ccw'
			MOTOR.stepperCONFIG(0,'A', motor1_direction,'H', motor1_velocity, 0 )
			MOTOR.stepperCONFIG(0,'B', motor2_direction,'H', motor2_velocity, 0 )
			MOTOR.stepperJOG(0,'A')
			MOTOR.stepperJOG(0,'B')
		else:
			MOTOR.stepperRATE(0,'A', motor1_velocity)
			MOTOR.stepperRATE(0,'B', motor2_velocity)
		current_time += 0.1
		time.sleep( 0.1 )
	MOTOR.stepperSTOP(0,'A')
	MOTOR.stepperSTOP(0,'B')
	return [motors_position[0] + command[0], motors_position[1] + command[1]]

def move( speed, command, motors_position ):
	return move_naive( speed, command, motors_position )
#	return move_smart( speed, command, motors_position )

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

def setangle(pwm, angle):
	#GPIO.output(4, True)
	pwm.ChangeDutyCycle( angle / 18 + 2.5 )
	time.sleep(0.5)
	#GPIO.output(4, False)
	#pwm.ChangeDutyCycle(0)
