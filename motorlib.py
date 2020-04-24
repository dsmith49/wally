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
	#print('move command:',speed, command)
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
	while(flag_a or flag_b):                     #start loop
		time.sleep(0.1)                           #check every 100msec
		stat=MOTOR.getINTflag0(0)                 #read interrupt flags
		if (stat & 2 ** 4): 
			flag_b=0
		if (stat & 2 ** 5):
			flag_a=0

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
	duty = angle / 18 + 2.5
	GPIO.output(4, True)
	pwm.ChangeDutyCycle(duty)
	time.sleep(0.5)
	GPIO.output(4, False)
	pwm.ChangeDutyCycle(0)
