import piplates.MOTORplate as MOTOR
import RPi.GPIO as GPIO
import time

def config( speed ):
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

def move( speed, command ):
	if (command[0] == 0 and command[1] == 0): return None
	motor1_direction = 'cw'
	motor2_direction = 'ccw'
	if (command[0] > 0): motor1_direction = 'ccw'
	if (command[1] > 0): motor2_direction = 'cw'
	MOTOR.stepperCONFIG(0,'A', motor1_direction,'H',speed,0)
	MOTOR.stepperCONFIG(0,'B', motor2_direction,'H',speed,0)
	MOTOR.stepperMOVE(0,'A', abs(command[0]))
	MOTOR.stepperMOVE(0,'B', abs(command[1]))

	flag_a=1                                      #Initialize flag to true
	flag_b=1
	while(flag_a or flag_b):                      #start loop
		time.sleep(0.1)                           #check every 100msec
		stat=MOTOR.getINTflag0(0)                 #read interrupt flags
		if (stat & 2 ** 4): 
			flag_b=0
		if (stat & 2 ** 5):
			flag_a=0

def motor_velocity_at_time( current_pos, end_pos, time ):
	x_diff   = end_pos[0] - current_pos[0]
	y_diff   = end_pos[1] - current_pos[1]
	velocity = x_diff**2 * time + x_diff * current_pos[0] + y_diff**2 * time + y_diff * current_pos[1]
	return velocity

def move2( current_position, end_position, x_total, speed ):

	x_diff      = end_position[0] - current_position[0]
	y_diff      = end_position[1] - current_position[1]
	distance    = ( x_diff**2 + y_diff]**2 )**0.5
	total_time  = distance / speed
	current_time = 0

	current_position_mirror = [ x_total - current_position[0], current_position[1] ]
	end_position_mirror     = [ x_total - end_position[0], end_position[1] ]

	while (current_time < total_time):
		motor1_velocity = motor_velocity_at_time( current_position, end_position, current_time )
		motor2_velocity = motor_velocity_at_time( current_position_mirror, end_position_mirror, current_time )
		if (current_time == 0):
			motor1_direction = 'cw'
			motor2_direction = 'ccw'
			if (motor1_velocity > 0): motor1_direction = 'ccw'
			if (motor2_velocity > 0): motor2_direction = 'cw'
			MOTOR.stepperCONFIG(0,'A', motor1_direction,'H', motor1_velocity, 0 )
			MOTOR.stepperCONFIG(0,'B', motor2_direction,'H', motor2_velocity, 0 )
			MOTOR.stepperJOG(0,'A')
			MOTOR.stepperJOG(0,'B')
		else:
			MOTOR.stepperRATE(0,'A', motor1_velocity))
			MOTOR.stepperRATE(0,'B', motor2_velocity))
		current_time += 0.1
		time.sleep( 0.1 )
	MOTOR.stepperSTOP(0,'A')
	MOTOR.stepperSTOP(0,'B')



def update_motors(motors_last_velocity, motors_velocity):
	if (motors_last_velocity[0]==0):
		motor1_direction = 'cw'
		if (motors_velocity[0] < 0): motor1_direction = 'ccw'
		MOTOR.stepperCONFIG(0,'A',motor1_direction,'H',abs(motors_velocity[0]),0)
		MOTOR.stepperJOG(0,'A')
	if (motors_last_velocity[1]==0):
		motor2_direction = 'ccw'
		if (motors_velocity[1] < 0): motor2_direction = 'cw'
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

def setangle(pwm, angle):
	#GPIO.output(4, True)
	pwm.ChangeDutyCycle( angle / 18 + 2.5 )
	time.sleep(0.5)
	#GPIO.output(4, False)
	#pwm.ChangeDutyCycle(0)
