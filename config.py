
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
pen_up_angle   = 22
pen_1_angle    = 10
pen_2_angle    = 20
pen_3_angle    = 30

svg_pixel_size = 1 #steps per pixel

