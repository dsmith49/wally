import json

class Config(object):

	def __init__(self):
		self.path            = '/home/pi/wally/'
		self.speed           = 350
		self.numlines        = 16                   # maximum number of horizontal lines per pixel
		self.smartmove       = 0
		self.crosshatch      = True             # not used yet
		self.boxsize_x       = 0.005
		self.boxsize_y       = 0.005      # pixel size width by height, in meters, used by smartmove
		self.boxsize = [self.boxsize_x, self.boxsize_y ]
		self.boxsize_naive   = [100,100]      # pixel size width by height, in steps, used by naivemove
		self.x_total         = 1.915                # distance between two motor wire mounts, in meters
		self.motor1_length   = 1.45		   # length of motor1 wire, in meters
		self.motor2_length   = 1.45           # length of motor2 wire, in meters (currently has to be the same as wire1)
		self.x_usable_start   = 0.70
		self.x_usable_stop    = 1.22        # not used yet
		self.y_usable_start   = 0.30
		self.y_usable_stop    = 1.00         # not used yet
		self.button_delay     = 0.05
		self.x_gondola        = 0.20
		self.y_gondola        = 0.04
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
		with open(self.path + 'config.json', 'w') as fp:
			json.dump( vars(self), fp, indent=2)

	def loadJSON(self):
		with open(self.path + 'config.json') as fp:
			data = json.load(fp)
			for key,value in data.items():
				setattr(self, key, type(getattr(self,key))(value))
		self.boxsize = [self.boxsize_x, self.boxsize_y ]

	def getJSON(self):
		return json.dumps( vars(self) )

	def putJSON(self, data ):
		for key,value in data.items():
			setattr(self, key, type(getattr(self,key))(value) )
		self.boxsize = [self.boxsize_x, self.boxsize_y ]
