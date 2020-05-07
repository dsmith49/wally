
speed = 200
numlines = 8                   # maximum number of horizontal lines per pixel
smartmove = True
crosshatch = False             # not used yet
boxsize   = [0.01,0.01]        # pixel size width by height, in meters
x_total = 1.915                # distance between two motor wire mounts, in meters
motor1_length = 1.56		   # length of motor1 wire, in meters
motor2_length = 1.56           # length of motor2 wire, in meters (currently has to be the same as wire1)
x_usable = [0.70,1.22]         # not used yet
y_usable = [0.30,1.00]         # not used yet
button_delay = 0.05
#meters_per_step = (2 * 0.025 * 3.14159) / 400 # = 0.00039269875 # meters per step # theoretical
meters_per_step = (0.55 / 13300) # = 0.00004135338  in practice
smart_step = 0.001
pen_down_angle = 15
pen_up_angle   = 20
pen_1_angle    = 10
pen_2_angle    = 20
pen_3_angle    = 30
