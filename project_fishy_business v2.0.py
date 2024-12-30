from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLUT.fonts import GLUT_BITMAP_HELVETICA_18
from OpenGL.GLU import *
import random

# Colors gula initiate korlam
white = (1.0, 1.0, 1.0)
red = (1.0, 0.0, 0.0)
teal = (0.0, 1.0, 1.0)
amber = (1.0, 0.75, 0.0)
green = (0.0, 1.0, 0.0)
background = (0.0, 0.0, 0.0)
pulse_frame_counter = 0
# Screen dimensions
width, height = 800, 800
game_state = 'menu'
my_fish_score = 20
fish_positions = []
higher_power = True


thrust_length = 15  # Initial length of the thrust flames
thrust_step = 1  # Step size for increasing or decreasing thrust length

# buttons
b_width, b_height = 120, 200
b_padding = 10

# circle
shooter_position = width // 2
shooter_position_y = 60
center_x, center_y = width //2, height // 2
radius = 20
cir_color = (1.0, 0.0, 0.0) #lal
# game_state = 'khelchi'
quit = False
fall_circle = [] # je britto gule niche porse
bubbles = [] # shape change kora britto ra
projectiles = []
score = 0
miss = 0 # miss kora cirlce gula
miss_shot = 0 #koto gula shot miss korsi
timer = False
game_mode = 'Day'


def fish_score_generator():
    global my_fish_score
    random_score = 50
    # check if my fish's score is in the beginner level
    if my_fish_score < 50:
        random_score = random.randint(30, 70)
    elif 50< my_fish_score < 100:
        random_score = random.randint(70, 150)
    elif 100< my_fish_score < 200:
        random_score = random.randint(150, 250)
    elif 200< my_fish_score < 300:
        random_score = random.randint(250, 350)
    elif 500< my_fish_score <1000:
        random_score = random.randint(500, 1500)
    elif 1000< my_fish_score < 2000:
        random_score = random.randint(1000, 2500)
    elif 2000< my_fish_score < 3000:
        random_score = random.randint(2000, 4000)
    else:
        # amar fisher score + 1500 ei range er moddhe ekta number ke append korvbe
        random_score = random.randint(my_fish_score, my_fish_score+1500)
    
    return random_score
# projectile shooter banabo
def draw_projectiles():
    glColor3f(1.0, 0.5, 0.0)
    for i,j, rad in projectiles:
        # draw_britto(i, j, rad)
        x = i
        y = j
        length = rad
        half_length = length // 1.25
        draw_midpoint_line(x, y, x, y + length*1.5)  # Vertical line
        draw_midpoint_line(x, y + length, x - half_length, y + half_length)  # Left diagonal
        draw_midpoint_line(x, y + length, x + half_length, y + half_length)

for i in range(5):
    score = fish_score_generator()
    decision_parameter = random.randint(0, 8)
    x = random.randint(25, width-25) # x er ekta andaje
    y = random.randint(665, 700) # random ekta y (ektu window bad diyem karon okhane amar shooter)
    rad = random.randint(20, 30) # random ekta radious
    is_pulsating = random.random() < 0.2 # 20% pulsing bubble add korbe 
    radius_step = 0.1
    if is_pulsating:
        radius_step = 2
    fall_circle.append([x, y, rad, is_pulsating, radius_step, score, decision_parameter])

def init():
    global game_mode
    glClearColor(0.0, 0.4, 0.6, 1.0)  # Blue background
    gluOrtho2D(0, width, 0, height)
    



# implement eight way symmetry
def zone_finder(x1, y1, x2, y2):
    dy = y2 - y1
    dx = x2 - x1
    if abs(dy) > abs(dx):
        if dy >= 0 and dx >= 0:
            return 1
        elif dy >= 0 and dx <= 0:
            return 2
        elif dy <= 0 and dx <= 0:
            return 5
        elif dy <= 0 and dx >= 0:
            return 6
    else:
        if dy >= 0 and dx >= 0:
            return 0
        elif dy >= 0 and dx <= 0:
            return 3
        elif dy <= 0 and dx <= 0:
            return 4
        elif dy <= 0 and dx >= 0:
            return 7
# eight way symmetry other to zero ------ zero to other (translate)
def symmetry_shunno_theke_onno(x0, y0, zone):
    if zone == 0:
        return x0, y0
    elif zone == 1: #1(y,x)
        return y0, x0
    elif zone == 2: #2(-y, x)
        return -y0, x0
    elif zone == 3: #3(-x, y)
        return -x0, y0
    elif zone == 4:
        return -x0, -y0
    elif zone == 5:
        return -y0, -x0
    elif zone == 6:
        return y0, -x0
    elif zone == 7:
        return x0, -y0

def symmetry_onno_theke_shunno(x1, y1, x2, y2, zone):
    if zone == 1:
        return y1, x1, y2, x2
    elif zone == 2:
        return y1, -x1, y2, -x2
    elif zone == 3:
        return -x1, y1, -x2, y2
    elif zone == 4:
        return -x1, -y1, -x2, -y2
    elif zone == 5:
        return -y1, -x1, -y2, -x2
    elif zone == 6:
        return -y1, x1, -y2, x2
    elif zone == 7:
        return x1, -y1, x2, -y2
    return x1, y1, x2, y2


def draw_britto(xcenter, ycenter, rad, color = cir_color):
    x = 0
    y = rad
    decision_parameter = 1 - rad #decision parameter
    glPointSize(3)
    glColor3f(*color)
    glBegin(GL_POINTS)

    plot_britto_points(xcenter, ycenter, x, y)

    while x<y:
        x = x + 1
        if decision_parameter < 0:
            decision_parameter = decision_parameter + (2* (x+1))
        else:
             y = y -1
             decision_parameter = decision_parameter + (2 * ((x-y)+1))
        plot_britto_points(xcenter, ycenter, x, y)
    
    glEnd()

def plot_britto_points(xcenter, ycenter, x, y):
     for zone in range(8):
        x_transformed, y_transformed = symmetry_shunno_theke_onno(x, y, zone)
        glVertex2f(xcenter + x_transformed, ycenter + y_transformed)



# midpoint line algo implement:
def draw_midpoint_line(xp1, yp1, xp2, yp2):
    original_zone = zone_finder(xp1, yp1, xp2, yp2)
    x1_0, y1_0, x2_0, y2_0 = symmetry_onno_theke_shunno(xp1, yp1, xp2, yp2, original_zone)

    dx = x2_0 - x1_0
    dy = y2_0 - y1_0
    d = 2 * dy - dx
    dE = 2 * dy
    dNE = 2 * (dy - dx)
    x = x1_0
    y = y1_0
    glPointSize(2)
    glBegin(GL_POINTS)
    while x <= x2_0:
        a, b = symmetry_shunno_theke_onno(x, y, original_zone)
        glVertex2f(a, b)
        if d < 0:
            x += 1
            d += dE
        else:
            x += 1
            y += 1
            d += dNE
    glEnd()

# arrow akano function
def arrow_akao(x, y, dir, size):
    scale = size / 60
    if dir == 'left':
        draw_midpoint_line(x - 20 * scale, y - 10 * scale, x - 30 * scale, y)  # Left
        draw_midpoint_line(x - 20 * scale, y + 10 * scale, x - 30 * scale, y)  # Right
        draw_midpoint_line(x - 30 * scale, y, x - 10 * scale, y)  # Base


# play pause akao
def playPause(x, y, size):
    scale = size / 60
    if game_state == 'khelchi':
        draw_midpoint_line(x - 10 * scale, y + 5 * scale, x - 10 * scale, y - 10 * scale)  # Left vertical line
        draw_midpoint_line(x + 10 * scale, y + 5 * scale, x + 10 * scale, y - 10 * scale)  # Right vertical line
    else:
        draw_midpoint_line(x - 10 * scale, y + 10 * scale, x + 10 * scale, y)  # Triangle 1
        draw_midpoint_line(x - 10 * scale, y - 10 * scale, x + 10 * scale, y)  # Triangle 2
        draw_midpoint_line(x - 10 * scale, y + 10 * scale, x - 10 * scale, y - 10 * scale)

# Cross akao 
def cross(x, y, size):
    scale = size / 60
    draw_midpoint_line(x - 10 * scale, y - 10 * scale, x + 10 * scale, y + 10 * scale) 
    draw_midpoint_line(x - 10 * scale, y + 10 * scale, x + 10 * scale, y - 10 * scale)  


# button gula akaite hobe
def button_akao():
    bt_w = b_width
    bt_h = b_height
    vertical_offset = 100

    #restart button
    res_x, res_y = 50, height - bt_h - 50 + vertical_offset
    glColor3f(*amber)
    arrow_akao(res_x + bt_w // 2, res_y + bt_h //2, 'left', bt_w)


    # play pause
    playPauseX = width // 2 -bt_w // 2
    playPauseY = height - b_height - 50 + vertical_offset
    glColor3f(*amber)
    playPause(playPauseX + bt_w // 2, playPauseY + bt_h //2, bt_w)
    
    # quit button
    QuitX = width - bt_w - 50
    QuitY = height - bt_h - 50 +vertical_offset
    glColor3f(*red)
    cross(QuitX + bt_w // 2, QuitY + bt_h //2, bt_w)

def midpoint_ellipse(rx, ry, xc, yc):
    """
    Midpoint ellipse algorithm to draw an ellipse centered at (xc, yc) with radii rx and ry.
    """
    x, y = 0, ry
    d1 = ry**2 - rx**2 * ry + 0.25 * rx**2
    dx = 2 * ry**2 * x
    dy = 2 * rx**2 * y

    # First region
    points = []
    while dx < dy:
        points.append((x + xc, y + yc))
        points.append((-x + xc, y + yc))
        points.append((x + xc, -y + yc))
        points.append((-x + xc, -y + yc))
        
        if d1 < 0:
            x += 1
            dx += 2 * ry**2
            d1 += dx + ry**2
        else:
            x += 1
            y -= 1
            dx += 2 * ry**2
            dy -= 2 * rx**2
            d1 += dx - dy + ry**2

    # Second region
    d2 = ry**2 * (x + 0.5)**2 + rx**2 * (y - 1)**2 - rx**2 * ry**2
    while y >= 0:
        points.append((x + xc, y + yc))
        points.append((-x + xc, y + yc))
        points.append((x + xc, -y + yc))
        points.append((-x + xc, -y + yc))
        
        if d2 > 0:
            y -= 1
            dy -= 2 * rx**2
            d2 += rx**2 - dy
        else:
            y -= 1
            x += 1
            dx += 2 * ry**2
            dy -= 2 * rx**2
            d2 += dx - dy + rx**2

    return points



import math
def draw_pixel(x, y):
    """
    Draw a single pixel using OpenGL points.
    """
    glBegin(GL_POINTS)
    glVertex2i(x, y)
    glEnd()


def draw_midpoint_ellipse(xc, yc, rx, ry):
    """
    Use the midpoint ellipse algorithm to draw an ellipse centered at (xc, yc) with radii rx and ry.
    """
    glColor3f(1.0, 0.0, 0.0)
    points = midpoint_ellipse(rx, ry, xc, yc)  # Get ellipse points using the midpoint algorithm
    for point in points:
        draw_pixel(point[0], point[1])  # Replace with your pixel-drawing logic

def draw_shooter():
    global shooter_position, shooter_position_y, my_fish_score
    x = shooter_position
    y = shooter_position_y
    body_length = 30  # Semi-major axis
    body_width = 20   # Semi-minor axis
    tail_width = 15
    tail_height = 20
    eye_radius = 3

    # Draw fish body (precise ellipse using midpoint algorithm)
    draw_midpoint_ellipse(x, y, body_width, body_length)

    # Draw fish tail (triangle placed correctly behind the body)
    glColor3f(1.0, 0.0, 0.0)  # Set color (green for the tail)
    tail_base_left_x = x - tail_width * 0.75
    tail_base_left_y = (y - body_length)-14
    tail_base_right_x = x + tail_width * 0.75
    tail_base_right_y = (y - body_length)-14
    tail_tip_x = x
    # tail_tip_y = y - body_length - tail_height
    tail_tip_y = y - (body_length//2 + tail_height//2)

    # Draw the tail triangle
    draw_midpoint_line(int(tail_base_left_x), int(tail_base_left_y), int(tail_tip_x), int(tail_tip_y))
    draw_midpoint_line(int(tail_base_right_x), int(tail_base_right_y), int(tail_tip_x), int(tail_tip_y))
    draw_midpoint_line(int(tail_base_left_x), int(tail_base_left_y), int(tail_base_right_x), int(tail_base_right_y))

    # Draw fish eye (circle)
    glColor3f(1.0, 1.0, 1.0)  # White for the eye
    eye_center_x = x
    eye_center_y = y + body_length * 0.3
    draw_britto(int(eye_center_x), int(eye_center_y), eye_radius, color=(1.0, 1.0, 1.0))  # Eye white

    # Draw fish pupil (smaller circle inside the eye)
    glColor3f(0.0, 0.0, 0.0)  # Black for the pupil
    draw_britto(int(eye_center_x), int(eye_center_y), int(eye_radius * 0.5), color=(0.0, 0.0, 0.0))  # Pupil

    # Display the score of the fish
    glColor3f(1.0, 1.0, 1.0)  # White color for the text
    glRasterPos2f(x - 10, y + 50)  # Position the text above the fish
    score_text = f"{my_fish_score}"
    for char in score_text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))



import random

# function to check overlapping
def is_overlapping(x1, y1, radius1, x2, y2, radius2):
    distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    return distance < (radius1 + radius2)
# print(fall_circle)
# adjust position
def add_fish(x, y, radius):
    for i in range(0, len(fall_circle)):
        fx, fy, fr, _, _, score, decision_parameter = fall_circle[i]
        j = fall_circle[i]
        if is_overlapping(x, y, radius, fx, fy, fr):
            # Adjust position to avoid overlap
            x += radius * 0.5
            y -= radius * 1
            # fall_circle[i] = [x, y, radius]
            prev1 = j[3]
            prev2 = j[4]
            fall_circle[i] = [x, y, radius, prev1, prev2, score, decision_parameter]

    # fish_positions.append((x, y, radius))

# mach gula re move koraitese
def randomly_move_fish():
    # here randomly move the falling fishes
    for i in range(len(fall_circle)):
        x, y, radius, is_pulsating, radius_step, score, decision_parameter = fall_circle[i]
        # Randomly move the fish within the screen
        x += random.randint(-6, 6)
        # y -= random.randint(1, 3)  # Move downwards with a random speed

        # Ensure the fish stays within the screen boundaries
        if x - radius < 0:
            x = radius
        elif x + radius > width:
            x = width - radius

        # if y - radius < 0:
        #     y = radius
        # elif y + radius > height:
        #     y = height - radius

        fall_circle[i] = [x, y, radius, is_pulsating, radius_step, score, decision_parameter]


##### will create some different kinds of fishes

def round_fish(x, y, radius, body_color):
    # Draw fish body
    draw_britto(x, y, radius, body_color)

    # Draw fish eye (fixed position relative to the fish)
    eye_color = (1.0, 1.0, 1.0)  # White eye
    eye_x = x + int(radius / 3)
    eye_y = y + int(radius / 3)
    eye_radius = int(radius / 4)
    draw_britto(eye_x, eye_y, eye_radius, eye_color)

    # Draw fish pupil (smaller circle inside the eye)
    pupil_color = (0.0, 0.0, 0.0)  # Black pupil
    pupil_radius = int(eye_radius / 2)
    draw_britto(eye_x, eye_y, pupil_radius, pupil_color)

    # Draw fish tail (triangle)
    tail_color = body_color
    tail_x1 = x - radius
    tail_y1 = y
    tail_x2 = x - int(radius * 1.5)
    tail_y2 = y - int(radius / 2)
    tail_x3 = x - int(radius * 1.5)
    tail_y3 = y + int(radius / 2)
    draw_triangle(tail_x1, tail_y1, tail_x2, tail_y2, tail_x3, tail_y3, tail_color)



def draw_starfish(x, y, size, color=(1.0, 1.0, 0.0)):
    """
    Draw a starfish with five arms and two eyes.
    """
    glColor3f(*color)
    angle_step = 72  # 360 degrees / 5 arms
    inner_radius = size // 2  # Radius for inner vertices

    # Compute star's outer and inner points
    points = []
    for i in range(10):  # Alternates between outer and inner points
        angle = i * (angle_step / 2) * (3.14159 / 180)
        radius = size if i % 2 == 0 else inner_radius
        x_point = x + radius * math.cos(angle)
        y_point = y + radius * math.sin(angle)
        points.append((x_point, y_point))

    # Draw lines connecting points
    for i in range(len(points)):
        x_start, y_start = points[i]
        x_end, y_end = points[(i + 1) % len(points)]  # Connect back to the first point
        draw_midpoint_line(int(x_start), int(y_start), int(x_end), int(y_end))

    # Add eyes to the starfish
    eye_offset = size // 3  # Distance from the center to the eyes
    eye_radius = size // 8  # Eye size
    # Left eye
    draw_britto(x - eye_offset, y + eye_offset, eye_radius, color=(1.0, 1.0, 1.0))  # White eye
    draw_britto(x - eye_offset, y + eye_offset, eye_radius // 2, color=(0.0, 0.0, 0.0))  # Black pupil
    # Right eye
    draw_britto(x + eye_offset, y + eye_offset, eye_radius, color=(1.0, 1.0, 1.0))  # White eye
    draw_britto(x + eye_offset, y + eye_offset, eye_radius // 2, color=(0.0, 0.0, 0.0))  # Black pupil


    # Draw lines connecting points
    for i in range(len(points)):
        x_start, y_start = points[i]
        x_end, y_end = points[(i + 1) % len(points)]  # Connect back to the first point
        draw_midpoint_line(int(x_start), int(y_start), int(x_end), int(y_end))


def draw_square_fish(x, y, size, color=(0.0, 1.0, 0.0)):
    glColor3f(*color)
    half_size = (size*1.5) // 2
    # Draw the body of the fish (square)
    draw_midpoint_line(x - half_size, y - half_size, x + half_size, y - half_size)  # Top side
    draw_midpoint_line(x + half_size, y - half_size, x + half_size, y + half_size)  # Right side
    draw_midpoint_line(x + half_size, y + half_size, x - half_size, y + half_size)  # Bottom side
    draw_midpoint_line(x - half_size, y + half_size, x - half_size, y - half_size)  # Left side

    # Draw the tail of the fish (triangle)
    tail_x1 = x - half_size
    tail_y1 = y
    tail_x2 = x - half_size - size // 2
    tail_y2 = y - size // 4
    tail_x3 = x - half_size - size // 2
    tail_y3 = y + size // 4
    draw_triangle(tail_x1, tail_y1, tail_x2, tail_y2, tail_x3, tail_y3, color)

    # Draw the eye of the fish (circle)
    eye_x = x + half_size // 2
    eye_y = y + half_size // 2
    eye_radius = size // 8
    draw_britto(eye_x, eye_y, eye_radius, color=(1.0, 1.0, 1.0))  # White eye
    draw_britto(eye_x, eye_y, eye_radius // 2, color=(0.0, 0.0, 0.0))  # Black pupil

def draw_shell(x, y, size, color=(1.0, 0.5, 0.0)):
        # Draw the shell using midpoint line algorithm
    # half_size = (size) // 2
    # for i in range(half_size):
    #     draw_midpoint_line(x - half_size + i, y - half_size, x + half_size - i, y + half_size)
    #     draw_midpoint_line(x - half_size, y - half_size + i, x + half_size, y + half_size - i)
    # draw_midpoint_line(x - half_size, y, x + half_size, y)
    # draw_midpoint_line(x, y - half_size, x, y + half_size)
    pass



def draw_snail(x, y, size, color=(0.5, 0.35, 0.05)):
    # Draw the snail's shell (spiral)
    glColor3f(*color)
    glBegin(GL_POINTS)
    for i in range(360 * 3):  # 3 full rotations
        angle = i * (3.14159 / 180)
        radius = size * (i / (360 * 3))
        x_point = x + radius * math.cos(angle)
        y_point = y + radius * math.sin(angle)
        glVertex2f(x_point, y_point)
    glEnd()

   

    # Draw the snail's eyes and pupils
    eye_radius = size * 0.1
    eye_x_offset = size * 0.3
    eye_y_offset = size * 0.5
    pupil_radius = eye_radius * 0.5
    draw_eyes(x, y, eye_radius, eye_x_offset, eye_y_offset, pupil_radius)


def draw_eyes(x, y, eye_radius, eye_x_offset, eye_y_offset, pupil_radius):
    for offset in [-eye_x_offset, eye_x_offset]:
        draw_britto(int(x + offset), int(y + eye_y_offset), int(eye_radius), color=(1.0, 1.0, 1.0))
        draw_britto(int(x + offset), int(y + eye_y_offset), int(pupil_radius), color=(0.0, 0.0, 0.0))




def draw_squid(x, y, size, color=(0.5, 0.5, 0.5)):
    # Draw the head of the squid (circle)
    head_radius = size // 1.25
    draw_britto(x, y, head_radius, color)

    # Draw the eyes of the squid (two small circles)
    eye_radius = head_radius // 4
    eye_x_offset = head_radius // 2
    eye_y_offset = head_radius // 2
    draw_britto(x - eye_x_offset, y + eye_y_offset, eye_radius, color=(1.0, 1.0, 1.0))
    draw_britto(x + eye_x_offset, y + eye_y_offset, eye_radius, color=(1.0, 1.0, 1.0))

    # Draw the pupils of the squid (smaller circles inside the eyes)
    pupil_radius = eye_radius // 2
    draw_britto(x - eye_x_offset, y + eye_y_offset, pupil_radius, color=(0.0, 0.0, 0.0))
    draw_britto(x + eye_x_offset, y + eye_y_offset, pupil_radius, color=(0.0, 0.0, 0.0))

    # # Draw the tentacles of the squid (lines)
    # tentacle_length = size*1.25
    # tentacle_count = 6
    # for i in range(tentacle_count):
    #     glColor3f(1.0, 1.0, 1.0)  # White color for the tentacles
    #     angle = (i - tentacle_count // 2) * (3.14159 / (tentacle_count // 2))
    #     tentacle_x = x + tentacle_length * math.cos(angle)
    #     tentacle_y = y - head_radius - tentacle_length * math.sin(angle)
    #     draw_midpoint_line(x, y - head_radius, int(tentacle_x), int(tentacle_y))


def draw_anglerfish(x, y, size, color=(1.0, 0.2, 0.5)):
    # Body
    draw_britto(x, y, size, color)

    # Glowing Orb
    orb_x = x + size + size // 2
    orb_y = y + size // 2
    draw_britto(orb_x, orb_y, size // 4, color=(1.0, 1.0, 1.0))

    # Connecting Line
    draw_midpoint_line(x + size, y, orb_x, orb_y)

    # Eye
    eye_x = x + size // 4
    eye_y = y + size // 3
    eye_radius = size // 6
    draw_britto(eye_x, eye_y, eye_radius, color=(1.0, 1.0, 1.0))
    draw_britto(eye_x, eye_y, eye_radius // 2, color=(0.0, 0.0, 0.0))

def draw_jellyfish(x, y, size, color=(0.8, 0.5, 1.0)):
    """
    Draw a jellyfish with a semi-circular body, tentacles, and two eyes.
    """
    # Body (semi-circle)
    draw_britto(x, y, size, color)

    # Tentacles
    for i in range(-3, 4):
        tentacle_x = x + i * (size // 4)
        tentacle_start_y = y - size
        tentacle_end_y = tentacle_start_y - size
        draw_midpoint_line(tentacle_x, tentacle_start_y, tentacle_x, tentacle_end_y)

    # Eyes
    eye_offset_x = size // 3  # Horizontal distance from the center
    eye_offset_y = size // 4  # Vertical position below the top of the body
    eye_radius = size // 8  # Eye size

    # Left eye
    draw_britto(x - eye_offset_x, y + eye_offset_y, eye_radius, color=(1.0, 1.0, 1.0))  # White eye
    draw_britto(x - eye_offset_x, y + eye_offset_y, eye_radius // 2, color=(0.0, 0.0, 0.0))  # Black pupil

    # Right eye
    draw_britto(x + eye_offset_x, y + eye_offset_y, eye_radius, color=(1.0, 1.0, 1.0))  # White eye
    draw_britto(x + eye_offset_x, y + eye_offset_y, eye_radius // 2, color=(0.0, 0.0, 0.0))  # Black pupil


def draw_clownfish(x, y, size, body_color=(1.0, 0.5, 0.0), stripe_color=(1.0, 1.0, 1.0)):
    # Body
    draw_britto(x, y, size+10, body_color)

    # Stripes
    stripe_width = size // 5
    draw_midpoint_line(x - stripe_width, y + size // 2, x - stripe_width, y - size // 2, stripe_color)
    draw_midpoint_line(x + stripe_width, y + size // 2, x + stripe_width, y - size // 2, stripe_color)

    # Eye
    eye_x = x + size // 2
    eye_y = y + size // 3
    eye_radius = size // 8
    draw_britto(eye_x, eye_y, eye_radius, color=(1.0, 1.0, 1.0))  # White eye
    draw_britto(eye_x, eye_y, eye_radius // 2, color=(0.0, 0.0, 0.0))  # Black pupil





        
def draw_falling_britto():
    # score = random.randint(90, 300)
    
    global fall_circle
    for i in fall_circle:
        # i.append(score)
        x, y, radius, is_pulsating, radius_step, score, decision_parameter = i
        # body_color = (random.random(), random.random(), random.random())  # Random color
        # draw_square_fish(x, y, radius, body_color)

        if decision_parameter == 0:
            body_color = (1.0, 0.5, 0.0)
            draw_starfish(x, y, radius, body_color)
        elif decision_parameter == 1:
            body_color = (0.0, 1.0, 0.0)
            round_fish(x, y, radius, body_color)
        elif decision_parameter == 2:
            body_color = (0.5, 0.5, 1.0)
            draw_squid(x, y, radius, body_color)
        elif decision_parameter == 3:
            body_color = (0.5, 0.2, .25)
            draw_square_fish(x, y, radius, body_color)
        
        elif decision_parameter == 4:
            # body_color = (0.8, 0.5, 1.0)
            draw_jellyfish(x, y, radius)

        elif decision_parameter == 5:
            # pass
            draw_anglerfish(x, y, radius)
        
        else:
            body_color = (1.0, 0.75, 0.8)
            draw_snail(x, y, radius, body_color)
            # draw_starfish(x, y, radius, body_color)
            

        # score of fishes
        glColor3f(1.0, 1.0, 1.0)  # White color for the text
        glRasterPos2f(x - 10, y + 50)  # Position the text above the fish
        score_text = f"{score}"
        for char in score_text:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))


def draw_triangle(x1, y1, x2, y2, x3, y3, color):
    glColor3f(*color)
    draw_midpoint_line(x1, y1, x2, y2)
    draw_midpoint_line(x2, y2, x3, y3)
    draw_midpoint_line(x3, y3, x1, y1)

# Button click operator
def button_click_control(x, y):
    global game_state, shooter_position, score, miss, miss_shot, projectiles, shooter_position_y
    button_w = b_width
    button_h = b_height
    vertical_offset = 70 # eigula old button_akao theke
    restX, restY = 50, height - b_height - 50 + vertical_offset # prev

    # game reset button press
    if restX <= x <= restX + b_width and restY <= y <= restY + b_height:
        reset_game()
    
    # pause button
    playPause_X = width // 2 -b_width // 2
    playPause_Y = height - b_height - 50 + vertical_offset
    if playPause_X <= x <= playPause_X + b_width and playPause_Y <= y <= playPause_Y + b_height:
        if game_state == 'khelchi':
            game_state = 'thamo'
        else:
            game_state = 'khelchi'
    
    # Quit button er kaj
    quitX = width - b_width -50
    quitY = height - b_height - 50 + vertical_offset
    if quitX <= x <= quitX + b_width and quitY <= y <= quitY + button_h:
        print("Game has been stopped")
        glutLeaveMainLoop()
        return

def reset_game():
    # mainly sob data clear kore reset kora lagbe
    global fall_circle, projectiles, score, miss, miss_shot, game_state, timer, shooter_position, shooter_position_y

    fall_circle.clear()
    projectiles.clear()
    shooter_position = width // 2
    score = 0
    miss = 0
    miss_shot = 0
    shooter_position_y = 50

    # notun kore falling cirlce
    for i in range(5):
        score = fish_score_generator()
        decision_parameter = random.randint(0, 8)
        x = random.randint(25, width-25) # x er ekta andaje
        y = random.randint(665, 700) # random ekta y (ektu window bad diyem karon okhane amar shooter)
        rad = random.randint(20, 30) # random ekta radious
        is_pulsating = random.random() < 0.2 # 20% pulsing bubble add korbe 
        radius_step = 0
        if is_pulsating:
            radius_step = 0.1
        fall_circle.append([x, y, rad, is_pulsating, radius_step, score, decision_parameter])

    
    game_state = 'khelchi'
    glutPostRedisplay()

    if not timer:
        glutTimerFunc(25, update, 0)
        timer = True

# take keyboad and mouse inputs
def mouse(button, state, x, y):
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        button_click_control(x, height - y)

def keyboard(key, x, y):
    global quit
    global shooter_position, shooter_position_y, game_state, game_mode
    
    if game_state == 'menu':
        if key == b's':  # Start game
            reset_game()
        elif key == b'q':  # Quit game
            print("Exiting game...")
            glutLeaveMainLoop()
        return
    increament = 10
    if key == b'a':
        shooter_position = shooter_position - increament # left side e jacche

        # corner case
        if shooter_position - 20 < 0:
            print("Cannot go left anymore")
            shooter_position = 20 # 20 hoche rocket er widht
    
    elif key == b'd':
        shooter_position = shooter_position + increament
        if shooter_position + 20 > width: # right e screen er baire na jay
            shooter_position = width - 20
    
    elif key == b' ':
        projectiles.append((shooter_position, shooter_position_y, 10))
    elif key == b'w':
        shooter_position_y = shooter_position_y + increament
        if shooter_position_y + 20 > height:
            shooter_position_y = height - 20
    elif key == b's':
        shooter_position_y = shooter_position_y - increament
        if shooter_position_y - 20 < 0:
            shooter_position_y = 20
    elif key == b'm':
        if game_mode == 'night':
            game_mode = 'day'
            glClearColor(0.0, 0.4, 0.6, 1.0) # blue
        else:
            game_mode = 'night'
            glClearColor(0.2, 0.2, 0.2, 1.0) # blackish
        

import math
# import numpy as np
def guli_khaise(C1X, C1Y, C1R, C2X, C2Y, C2R):
    # guli ar ball er modder radius er distance calculate kora lagbe
    # d = root((x2 - x1)^2 + (y2 - y1)^2)
    radius_2_radius = math.sqrt((C2X - C1X)**2 + (C2Y- C1Y)**2)
    flag = 0

    if radius_2_radius < (C1R + C2R):
        flag = True
    else:
        flag = False
    return flag

def rect_circle_collision(rx, ry, rw, rh, cx, cy, cr):
    # Find the closest point on the rectangle to the circle's center
    closest_x = max(rx, min(cx, rx + rw))
    closest_y = max(ry, min(cy, ry + rh))
    
    # Calculate the distance from the circle's center to this closest point
    distance = math.sqrt((cx - closest_x) ** 2 + (cy - closest_y) ** 2)
    
    # Check if the distance is less than the circle's radius
    return distance < cr




def update(value):
    global pulse_frame_counter, fall_circle, projectiles, game_state, height, width, score, miss, miss_shot, timer, my_fish_score, higher_power, shooter_position_y
    global thrust_length, thrust_step
    if game_state == 'thamo':
        glutTimerFunc(25, update, 0)
        return

    if game_state == 'khelchi':
        pulse_frame_counter += 1
        new_guli = []
        thrust_length += thrust_step
        if thrust_length > 25 or thrust_length < 15:  # Oscillate between 15 and 25
            thrust_step = -thrust_step

        for guli in projectiles:
            guliX, guliY, guliR = guli
            guli_lagse = False

            for i in range(len(fall_circle) - 1, -1, -1):
                FallCircleX, FallCircleY, FallR, is_pulsating, radius_step, score, decision_parameter = fall_circle[i]
                if guli_khaise(FallCircleX, FallCircleY, FallR, guliX, guliY, guliR):
                    if is_pulsating and my_fish_score <= score:
                        # score += 5
                        fall_circle[i][5] = score - 10
                        print("You hit a pulsing fish!")
                    elif my_fish_score <= score:
                        # score += 1
                        fall_circle[i][5] = score - 5
                    else:
                        pass
                    # print(f"Score: {score}")
                    # fall_circle.pop(i)
                    guli_lagse = True

                    # Generate a new circledd

                    # Nscore = random.randint(90, 300)
                    # Ndecision_parameter = random.randint(0, 6)
                    # Nx = random.randint(25, width - 25)
                    # Ny = random.randint(665, 700)
                    # Nrad = random.randint(20, 30)
                    # Nis_pulsating = random.random() < 0.2
                    # Nradius_step = 0.1 if Nis_pulsating else 0
                    # fall_circle.append([Nx, Ny, Nrad, Nis_pulsating, Nradius_step, Nscore, Ndecision_parameter])
                    break

            if not guli_lagse:
                Ny = guliY + 40
                if Ny < height:
                    new_guli.append((guliX, Ny, guliR))
                else:
                    miss_shot += 1
                    print(f"Missed shots : {miss_shot}")  # Missed shot

        projectiles = new_guli

    # Update falling circles
    for i in range(len(fall_circle)):
        Fx, Fy, rad, is_pulsating, radius_step, score, decision_parameter = fall_circle[i]
        Fy -= 0.8  # Move down
        if is_pulsating and pulse_frame_counter % 15 == 0:
            # print(f"Creating pulsing Bubble, radius is {rad}, radius step is {radius_step}")
            if rad < 10:
                rad = rad + 10
            rad += (radius_step+ 2)
            if rad > 30 or rad < 21:  # Pulse limits
                # print("Entered here !")
                radius_step = -(radius_step + 5)
                # print(f"Current radius step: {radius_step}")
        if Fy + rad < 0:  # Circle exits screen
            Fx = random.randint(25, width - 25)
            # Fy = random.randint(rad, width - rad)
            Fy = height - 25
            miss += 1
        fall_circle[i] = [Fx, Fy, rad, is_pulsating, radius_step, score, decision_parameter]
        # print(fall_circle)

        # Check for collision with shooter
        shooter_x = shooter_position - 10
        shooter_y = shooter_position_y - 20
        shooter_width = 20
        shooter_height = 40
        if rect_circle_collision(shooter_x, shooter_y, shooter_width, shooter_height, Fx, Fy, rad):
            if my_fish_score > score: # amar fish er score beshi
                my_fish_score = my_fish_score + score
                print(f"Score: {my_fish_score}")
                fall_circle.pop(i)
                # guli_lagse = True

                    # Generate a new fish
                Nscore = fish_score_generator()
                Ndecision_parameter = random.randint(0, 8)
                Nx = random.randint(25, width - 25)
                Ny = height - 25
                Nrad = random.randint(20, 30)
                Nis_pulsating = random.random() < 0.2
                Nradius_step = 0.1 if Nis_pulsating else 0
                fall_circle.append([Nx, Ny, Nrad, Nis_pulsating, Nradius_step, Nscore, Ndecision_parameter])
            else:
                game_state = 'Shesh'
                fall_circle.clear()
                glutPostRedisplay()
                print("Game Over, fish got involved in Fishy business with bigger fish :(")
                higher_power = True
                print(f"Final Score: {my_fish_score}")
                # my_fish_score = 20
                break
            
        if miss_shot >=5:
                game_state = 'Shesh'
                fall_circle.clear()
                glutPostRedisplay()
                print("Game Over: 5 Shot Miss!")
                print(f"Final Score: {my_fish_score}")
                # my_fish_score = 20
                # draw_text(width//2 - 70, 500, "GAME OVER", font=GLUT_BITMAP_HELVETICA_18, color=(1,0,0))
                # draw_text(width//2 - 70, 500, f"Final Score: {score}", font=GLUT_BITMAP_HELVETICA_18, color=(1,1,1))
                break

        # if miss >= 3:
        #     game_state = 'Shesh'
        #     fall_circle.clear()
        #     glutPostRedisplay()
        #     print("Game Over: 3 Circle Miss!")
        #     print(f"Final Score: {score}")
        #     # game_over(score)
        #     break

    if game_state != 'Shesh':
        glutPostRedisplay()
        glutTimerFunc(25, update, 0)
    else:
        timer = False


def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18, color=(0.0,0.0,0.0)):
    
    # glColor3f(*color)
    glColor3f(1.0, 1.0, 1.0)
    glRasterPos2f(x, y)
    text = text
    for char in text:
        glutBitmapCharacter(font, ord(char))


def display():
    global my_fish_score, higher_power, miss_shot, game_mode
    glClear(GL_COLOR_BUFFER_BIT)

    if game_state == 'menu':
        draw_text(width // 2 - 70, height // 2 + 20, "Fishy Business", GLUT_BITMAP_HELVETICA_18, (1.0, 1.0, 1.0))
        # Static menu options
        draw_text(width // 2 - 70, height // 2 - 20, "Press S to Start", GLUT_BITMAP_HELVETICA_18, (1.0, 1.0, 1.0))
        draw_text(width // 2 - 70, height // 2 - 60, "Press Q to Quit", GLUT_BITMAP_HELVETICA_18, (1.0, 1.0, 1.0))
        draw_text(width // 2 - 300, height // 2 - 200, "*****Game Rules*****", GLUT_BITMAP_HELVETICA_18, (1.0, 1.0, 1.0))
        draw_text(width // 2 - 300, height // 2 - 220, "1. Press a, s, d, w to move your fish.", GLUT_BITMAP_HELVETICA_18, (1.0, 1.0, 1.0))
        draw_text(width // 2 - 300, height // 2 - 240, "2. Press spacebar to shoot your opponent fish.", GLUT_BITMAP_HELVETICA_18, (1.0, 1.0, 1.0))
        draw_text(width // 2 - 300, height // 2 - 260, "3. Shooting will decrease the opponent fish's power.", GLUT_BITMAP_HELVETICA_18, (1.0, 1.0, 1.0))	
        draw_text(width // 2 - 300, height // 2 - 280, "4. Do not waste more than 5 bullets.", GLUT_BITMAP_HELVETICA_18, (1.0, 1.0, 1.0))
        draw_text(width // 2 - 300, height // 2 - 300, "5.Do not try to be Walter White and Kill a bigger fish. If you do, you will Break Badly.", GLUT_BITMAP_HELVETICA_18, (1.0, 1.0, 1.0))
        glutSwapBuffers()
        return
        # menu()
    # Draw Score and Missed Fish
    # draw_text(10, 10, f"Score: {my_fish_score}", GLUT_BITMAP_HELVETICA_18, (1,1,1))
    m = width // 2
    draw_text(m-400, 20, f"Score: {my_fish_score}", GLUT_BITMAP_HELVETICA_18, (0, 0, 0))
    draw_text(m-400, 40, f"Missed Shots: {miss_shot}", GLUT_BITMAP_HELVETICA_18, (0, 0, 0))
    draw_text(m-400, 60, f"Game Mode: {game_mode}", GLUT_BITMAP_HELVETICA_18, (0, 0, 0))
    # # draw_text(10, 30, f"Power: {player_power}", GLUT_BITMAP_HELVETICA_18, (1,1,0))
    # draw_text(10, 50, f"Missed: {miss_shot}", GLUT_BITMAP_HELVETICA_18, (1,0.5,0.5))
    
    if game_state == 'Shesh':
        #Game Over Screen
        draw_text(width//2 - 70, height//2 + 20, "GAME OVER", font=GLUT_BITMAP_HELVETICA_18, color=(1,0,0))
        draw_text(width//2 - 70, height//2 - 20, f"Final Score: {my_fish_score}", font=GLUT_BITMAP_HELVETICA_18, color=(1,1,1))
        button_akao()
        if miss_shot >= 5:
            draw_text(width//2 - 250, height//2 - 60, "5 Shot Miss! You cannot spare bullets in a hostile world", font=GLUT_BITMAP_HELVETICA_18, color=(1,0,0))
            button_akao()
        elif higher_power:
            draw_text(width//2 - 250, height//2 - 60, "Game Over, fish got involved in Fishy business with bigger fish :(", font=GLUT_BITMAP_HELVETICA_18, color=(1,0,0))
            higher_power = False
            button_akao()
        glutSwapBuffers()
        my_fish_score = 20
        return
    
    
    button_akao()
    draw_shooter()
    draw_falling_britto()
    randomly_move_fish()
    draw_projectiles()
    glutSwapBuffers()
    

glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(width, height)
glutInitWindowPosition(100, 100)
glutCreateWindow(b"Fishy Business")
init()  # Set up initial OpenGL environment
glutDisplayFunc(display)  # Register display callback
glutMouseFunc(mouse)  # Register mouse click callback
glutKeyboardFunc(keyboard)  # Register keyboard for special keys
glutTimerFunc(25, update, 0)  # Initially register the timer callback to start updates
glutMainLoop()