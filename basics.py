import sys
import pygame
from pygame.locals import *
pygame.init()

pygame.display.set_caption('potigame')
WINDOW_SIZE = (960, 540)
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
display = pygame.Surface(WINDOW_SIZE)

clock = pygame.time.Clock()

player_image = pygame.image.load('player-1.png')
player_image.set_colorkey((255, 255, 255, 255))
ground_image = pygame.image.load('ground-1.png')
shop_image = pygame.image.load('shop.png')
shopp = pygame.transform.scale(shop_image, (shop_image.get_width()*2, shop_image.get_height()*2))

bg1_image = pygame.image.load('background_layer_1.png')
bg2_image = pygame.image.load('background_layer_2.png')
bg3_image = pygame.image.load('background_layer_3.png')

def load_map(path):
    f = open(path+".txt", "r")
    data = f.read()
    f.close()
    data = data.split('\n')
    game_map = []
    for row in data:
        game_map.append(list(row))
    return game_map

game_map = load_map('map')

def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list

def move(rect, movement, tiles):
    collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}

    rect.x += movement[0]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True

    rect.y += movement[1]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True

    return rect, collision_types

moving_right = False
moving_left = False

player_location = [50, 50]
player_y_momentum = 0
player_is_jumping = False
velocity = 0.17

true_scroll = [0,0]

TILE_SIZE = ground_image.get_width()

player_rect = pygame.Rect(50, 50, player_image.get_width(), player_image.get_height())
test_rect = pygame.Rect(100, 100, 100, 50)

print("TILE SIZE "+str(TILE_SIZE))

FACTOR_SCALE = 3
PLAYER_MOVEMENT_SPEED = 8

#   draw background
image = pygame.transform.scale(bg1_image, (bg1_image.get_width()*FACTOR_SCALE, bg1_image.get_height()*FACTOR_SCALE))
image2 = pygame.transform.scale(bg2_image, (bg2_image.get_width()*FACTOR_SCALE, bg2_image.get_height()*FACTOR_SCALE))
image3 = pygame.transform.scale(bg3_image, (bg3_image.get_width()*FACTOR_SCALE, bg3_image.get_height()*FACTOR_SCALE))

run = True
while run:
    # paint background
    display.fill((146,244,255))

    true_scroll[0] += (player_rect.x-true_scroll[0]-450)/20
    true_scroll[1] += (player_rect.y-true_scroll[1]-350)/20

    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    display.blit(image, (0, 0))
    display.blit(image2, (0, 0))    
    display.blit(image3, (0, 0))

    tile_rects = []

    #   display tiles and things and 
    y = 0
    for row in game_map:
        x = 0
        for tile in row:
            if tile == '1':
                display.blit(ground_image, (x * TILE_SIZE-scroll[0], y * TILE_SIZE-scroll[1]))
            if tile == '2':
                display.blit(shopp, (x * TILE_SIZE-scroll[0], y * TILE_SIZE-scroll[1]))
            if tile not in ['0', '2']:
                tile_rects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            x += 1
        y += 1



    player_movement = [0,0]
    if moving_right:
        player_movement[0] += PLAYER_MOVEMENT_SPEED
    if moving_left:
        player_movement[0] -= PLAYER_MOVEMENT_SPEED

    player_movement[1] += player_y_momentum
    player_y_momentum += velocity

    if player_y_momentum > 10:
        player_y_momentum = 10

    player_rect, collisions = move(player_rect, player_movement, tile_rects)
    if collisions['bottom']:
        player_is_jumping = False
        player_y_momentum = 0

    #   draw player sprite
    display.blit(player_image, (player_rect.x-scroll[0], player_rect.y-scroll[1]))


    #   event handler
    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                moving_right = True
            if event.key == K_LEFT:
                moving_left = True
            if event.key == K_UP and not player_is_jumping:
                player_is_jumping = True
                player_y_momentum = -5
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                moving_right = False
            if event.key == K_LEFT:
                moving_left = False
            
    
    # screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0,0))
    screen.blit(display, (0,0))
    pygame.display.update()
    clock.tick(60)
    # print(clock.get_fps())