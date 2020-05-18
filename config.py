import json

class Config(object):

	def __init__(self):
		self.speed           = 350
		self.numlines        = 16                   # maximum number of horizontal lines per pixel
		self.smartmove       = False
		self.crosshatch      = True             # not used yet
		self.boxsize         = [0.005,0.005]      # pixel size width by height, in meters, used by smartmove
		self.boxsize_naive   = [100,100]      # pixel size width by height, in steps, used by naivemove
		self.x_total         = 1.915                # distance between two motor wire mounts, in meters
		self.motor1_length   = 1.45		   # length of motor1 wire, in meters
		self.motor2_length   = 1.45           # length of motor2 wire, in meters (currently has to be the same as wire1)
		self.x_usable        = [0.70,1.22]         # not used yet
		self.y_usable        = [0.30,1.00]         # not used yet
		self.button_delay    = 0.05
		self.x_gondola       = 0.10
		self.y_gondola       = 0.04
		#self.meters_per_step = (2 * 0.025 * 3.14159) / 400 # = 0.00039269875 # meters per step # theoretical
		self.meters_per_step = (0.55 / 13300) # = 0.00004135338  in practice
		self.smart_step      = 0.01              # meters per step
		self.pen_down_angle  = 18
		self.pen_up_angle    = 21
		self.pen_1_angle     = 10
		self.pen_2_angle     = 20
		self.pen_3_angle     = 30
		self.svg_pixel_size  = 12 #steps per pixel

	def writeJSON(self):
		with open('config.json', 'w') as fp:
			json.dump( vars(self), fp)

	def loadJSON(self):
		with open('config.json') as fp:
			data = json.load(fp)
			for key,value in data.items():
				setattr(self, key, value)

	def getJSON(self):
		return json.dump( vars(self) )


speed = 350
numlines = 16                   # maximum number of horizontal lines per pixel
smartmove = False
crosshatch = True             # not used yet
boxsize   = [0.005,0.005]      # pixel size width by height, in meters, used by smartmove
boxsize_naive = [100,100]      # pixel size width by height, in steps, used by naivemove
x_total = 1.915                # distance between two motor wire mounts, in meters
motor1_length = 1.45		   # length of motor1 wire, in meters
motor2_length = 1.45           # length of motor2 wire, in meters (currently has to be the same as wire1)
x_usable = [0.70,1.22]         # not used yet
y_usable = [0.30,1.00]         # not used yet
button_delay = 0.05
x_gondola = 0.10
y_gondola = 0.04
#meters_per_step = (2 * 0.025 * 3.14159) / 400 # = 0.00039269875 # meters per step # theoretical
meters_per_step = (0.55 / 13300) # = 0.00004135338  in practice
smart_step = 0.01              # meters per step
pen_down_angle = 18
pen_up_angle   = 21
pen_1_angle    = 10
pen_2_angle    = 20
pen_3_angle    = 30

svg_pixel_size = 12 #steps per pixel

