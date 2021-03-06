import ctypes
from math import sqrt
import pygame
import color
import source
from src.sprites import background, player, menubutton, platform, splash

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
fps = 60

# Enable loops
menu_running = True
game_running = True

# Main Menu Splash and Background
title_splash = splash.Splash(source.splash('splash.png'), resolution)
menu_background = background.Background(source.background('menu_bg.png'),display_height)
splashes = pygame.sprite.Group()
backgrounds = pygame.sprite.Group()
splashes.add(title_splash), backgrounds.add(menu_background)

# Menu Buttons
buttons = pygame.sprite.Group()
start_button = menubutton.MenuButton(resolution, display_height / 2, text='Start')
quit_button = menubutton.MenuButton(resolution, display_height / 2 + (start_button.height * 1.5), text='Quit')

buttons.add(start_button, quit_button)

all_menu_sprites = pygame.sprite.Group()
all_menu_sprites.add(buttons, title_splash, menu_background)

while menu_running:
    # Get mouse position
    pos = pygame.mouse.get_pos()

    # Check Events
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                menu_running = game_running = False
        if event.type == pygame.MOUSEBUTTONUP:
            print event
            if start_button.rect.collidepoint(pos):
                menu_running = False
            if quit_button.rect.collidepoint(pos):
                menu_running = game_running = False
        if event.type == pygame.QUIT:
            menu_running = game_running = False

    # Set cursor
    hovered_buttons = [b for b in buttons if b.rect.collidepoint(pos)]
    if len(hovered_buttons) > 0:
        pygame.mouse.set_cursor(*pygame.cursors.diamond)
    else:
        pygame.mouse.set_cursor(*pygame.cursors.arrow)

    display.fill(color.white)

    backgrounds.draw(display)
    splashes.draw(display)
    buttons.draw(display)

    all_menu_sprites.update()

    pygame.display.update()
    clock.tick(fps)


# Sprite Groups
players = pygame.sprite.Group()
backgrounds = pygame.sprite.Group()
platforms = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

# Player and Background
player = player.Player(source.player('zach_proto.png'), display_height)
background = background.Background(source.background('bgtest.png'), display_height)

# Platforms
floor = platform.Platform(color.dark_green, (background.width, background.height / 25), (0, background.height - background.height / 25))
plat_1 = platform.Platform(color.grey, (display_width / 7, display_height / 25), (background.width / 2, display_height / 2))

# Add sprites to groups
players.add(player)
backgrounds.add(background)
platforms.add(floor,plat_1)
all_sprites.add(players,backgrounds,platforms)

# Game Vars
playerX, playerY = display_width/8, display_height/2
left_coord, right_coord = 0, display_width
dx, dy, bg_x = 0, 0, 0
jumping = False
jump_count = 0
max_jump = 2
jump_speed = -display_height/43.2
fall_acceleration = display_height/1440.0
move_speed = display_width/256.0
far_left , far_right = True, False

down_collision_buffer = display_height / sqrt(720)
up_collision_buffer = -jump_speed * 1.5
side_collision_buffer = move_speed

active_key = None


def change_x(key):
    keys = {None:0, pygame.K_LEFT:-move_speed, pygame.K_RIGHT:move_speed}
    return keys[key]

# Game loop
while game_running:
    # Hide cursor
    pygame.mouse.set_visible(False)
    # Check Events
    for event in pygame.event.get():
        # User closes window
        if event.type == pygame.QUIT:
            game_running = False
        # Key Press Events
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # Quit game
                game_running = False
            if event.key == pygame.K_SPACE:
                # Jump
                if jump_count<2:
                    dy, jumping = jump_speed, True
                    jump_count += 1
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                # Move left
                active_key = pygame.K_LEFT
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                # Move right
                active_key = pygame.K_RIGHT
        if event.type == pygame.KEYUP:
            # Key-up behaviour to prevent sticky key effect by only canceling
            # movement if player is moving in the direction of the key being released
            if ((event.key == pygame.K_RIGHT or event.key == pygame.K_d) and dx == move_speed) or \
                    ((event.key == pygame.K_LEFT or event.key == pygame.K_a) and dx == -move_speed):
                active_key = None

    # Set change in x
    dx = change_x(active_key)

    # Move platforms into place
    for platform in platforms:
        # Set platform x if on screen (y is set in the constructor)
        if left_coord<platform.x<right_coord:
            platform.rect.x = platform.x-left_coord

    # Check platform collisions
    platform_collisions = pygame.sprite.spritecollide(player, platforms, False)
    if len(platform_collisions) != 0 and not jumping:
        for collision in platform_collisions:
            # Top collision
            if playerY+player.height<collision.rect.y+down_collision_buffer:
                playerY = collision.rect.y-player.height+1
                dy = 0
                jump_count = 0
            # Bottom collision
            elif playerY > collision.rect.y - up_collision_buffer:
                playerY += up_collision_buffer/4
                dy = 0
            # Left or Right collision
            elif playerX + player.width + side_collision_buffer > collision.rect.x or \
                    playerX < collision.rect.x + collision.rect.width + side_collision_buffer:
                dx = 0
                dy += fall_acceleration
    else:
        jumping = False
        dy += fall_acceleration

    # Update y position
    playerY += dy
    if playerY > display_height-player.height:
        playerY = display_height-player.height
    if playerY < 0:
        playerY = dy = 0

    # Update x position
    if playerX == (display_width-player.width)/2:
        bg_x -= dx
    if not(far_left or far_right):
        playerX = (display_width-player.width)/2
        left_coord += dx
        right_coord += dx
    else:
        playerX += dx

    # Boundary collisions
    if playerX<0:
        playerX = 0
    elif playerX>display_width-player.width:
        playerX = display_width-player.width

    # Update background
    if bg_x >= 0:
        far_left, far_right = True, False
        bg_x = 0
    elif bg_x <= display_width-background.width:
        far_right, far_left = True, False
        bg_x = display_width-background.width
    else:
        far_left = far_right = False

    # Draw and tick
    player.rect.x = playerX
    player.rect.y = playerY

    background.rect.x = bg_x
    background.rect.y = 0

    backgrounds.draw(display)
    platforms.draw(display)
    players.draw(display)

    all_sprites.update()

    pygame.display.update()
    clock.tick(fps)


pygame.quit()