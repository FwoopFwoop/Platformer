import pygame
import ctypes
from math import ceil
# Color Declarations
black = 0, 0, 0
white = 255,255,255

# Initialize pygame components
pygame.init()

# Obtain Screen Size
user32 = ctypes.windll.user32
resolution = (display_width , display_height) = (user32.GetSystemMetrics(0),user32.GetSystemMetrics(1))
# Create display surface
display = pygame.display.set_mode(resolution,pygame.FULLSCREEN)
# Set window title
pygame.display.set_caption('PyPlatformer')
# Create Clock
clock = pygame.time.Clock()

# Zach Image
zach_img = pygame.image.load('zach.png')
zach_ratio = float(zach_img.get_rect().size[1]/zach_img.get_rect().size[0])
zach_height = display_height/6
zach_width = int(ceil(zach_ratio*zach_height))
zach_img = pygame.transform.scale(zach_img, (zach_width,zach_height))


# Background
bg_img = pygame.image.load('bgtest.png')
bg_ratio = float(bg_img.get_rect().size[0]/bg_img.get_rect().size[1])
bg_height = display_height
bg_width = int(ceil(bg_height*bg_ratio))
bg_img = pygame.transform.scale(bg_img, (bg_width, bg_height)).convert()


def bg(pos):
    display.blit(bg_img,(pos, 0))


def zach(x,y):
    # Draw at coordinates, accouting for image width and height
    display.blit(zach_img,(x-zach_width/2,y-zach_height))


# Determines whether or not Zach is on a surface.
def on_platform(x,y):
    # TODO
    if y >= display_height:
        return True
    else:
        return False

# Game Vars
playerX, playerY =  display_width/8, display_height
position = playerX
dx, dy, bg_x = 0, 0, 0
jumping = False
jump_speed = -display_height/43.2
fall_acceleration = display_height/1440.0
double_jump_buffer = display_height/216.0
move_speed = display_width/256.0
far_left , far_right = True, False

isRunning = True


# Game loop
while isRunning:

    # Check Events
    for event in pygame.event.get():
        # User closes window
        if event.type == pygame.QUIT:
            isRunning = False
        # Key Press Events
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False
            if event.key == pygame.K_SPACE:
                if abs(dy)<double_jump_buffer:
                    dy, jumping = jump_speed, True
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                dx = -move_speed
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                dx = move_speed
        if event.type == pygame.KEYUP:
            if ((event.key == pygame.K_RIGHT or event.key == pygame.K_d) and dx == move_speed) or \
                    ((event.key == pygame.K_LEFT or event.key == pygame.K_a) and dx == -move_speed):
                dx = 0

    # Player Y
    if on_platform(playerX,playerY) and not jumping:
        dy = 0
    else:
        jumping = False
        dy += fall_acceleration

    # Update y position
    playerY += dy
    if playerY > display_height:
        playerY = display_height
    if playerY < zach_height:
        playerY, dy = zach_height, 0

    # Update x position
    if playerX == display_width/2:
        bg_x -= dx
    if not(far_left or far_right):
        playerX = display_width/2
    else:
        playerX += dx

    # Boundary collisions
    if playerX<zach_width/2:
        playerX = zach_width/2
    elif playerX>display_width-zach_width/2:
        playerX = display_width-zach_width/2
    else:
        # Update Absolute Position
        position += dx

    # Update background
    if bg_x >= 0:
        far_left, far_right = True, False
        bg_x = 0
    elif bg_x <= display_width-bg_width:
        far_right, far_left = True, False
        bg_x = display_width-bg_width
    else:
        far_left = far_right = False

    # Draw and tick
    bg(bg_x)
    zach(playerX, playerY)
    pygame.display.update()
    clock.tick(60)

pygame.quit()