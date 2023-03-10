import sys
import pygame
from pygame.locals import *
from pygame import mixer

pygame.init()
mixer.init()

mixer.music.load('lloyd.wav')

mixer.music.set_volume(0.2)

pygame.display.set_caption('capi the game')
WINDOW_SIZE = (800, 400)
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
display = pygame.Surface(WINDOW_SIZE)

clock = pygame.time.Clock()

ground_image = pygame.image.load('ground-1.png')
shop_image = pygame.image.load('shop.png')
shopp = pygame.transform.scale(shop_image, (shop_image.get_width()*2, shop_image.get_height()*2))

bg1_image = pygame.image.load('clouds/1.png')
bg2_image = pygame.image.load('clouds/6.png')
bg3_image = pygame.image.load('clouds/2.png')
bg4_image = pygame.image.load('clouds/4.png')
bg4_image.set_alpha(200)
bg5_image = pygame.image.load('clouds/5.png')

single_cloud_image = pygame.image.load('clouds/3.png')
single_cloud_image.set_alpha(230)

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

global animation_frames
animation_frames = {}

def load_animation(path, frame_durations):
    global animation_frames
    animation_name = path.split('/')[-1]
    animation_frame_data = []
    n = 0
    for frame in frame_durations:
        animation_frame_id = animation_name+'-'+str(n)
        img_location = path+'/'+animation_frame_id+'.png'
        animation_image = pygame.image.load(img_location).convert()
        animation_image.set_colorkey((255, 255, 255, 255))
        animation_frames[animation_frame_id] = animation_image.copy()
        for i in range(frame):
            animation_frame_data.append(animation_frame_id)
        n += 1
    return animation_frame_data

def change_action(action_var, frame, new_value):
    if action_var != new_value:
        action_var = new_value
        frame = 0
    return action_var,frame

#   load animation database
animation_database = {}
animation_database['walk'] = load_animation('capy/walk', [4,4,4,4,4,4,4,4])
animation_database['sitting-idle'] = load_animation('capy/sitting-idle', [4,4,4,4,4,4,4,4])
animation_database['munch'] = load_animation('capy/munch', [4,4,4,4,4,4,4,4])

player_action = 'walk'
player_frame = 0
player_flip = False

moving_right = False
moving_left = False
moving_up = False
moving_down = False

player_location = [20, 20]
player_y_momentum = 0
player_is_jumping = False
velocity = 0.2

true_scroll = [0,0]

TILE_SIZE = ground_image.get_width()
TILE_SIZE_SCALE = TILE_SIZE*0.5
ground_image_resized = pygame.transform.scale(ground_image,(TILE_SIZE_SCALE, TILE_SIZE_SCALE))

player_rect = pygame.Rect(200, 200, 64, 45)

print("TILE SIZE "+str(TILE_SIZE))

FACTOR_SCALE = 1.4
PLAYER_MOVEMENT_SPEED = 5

#   draw background
image = pygame.transform.scale(bg1_image, (bg1_image.get_width()*FACTOR_SCALE, bg1_image.get_height()*FACTOR_SCALE))
image2 = pygame.transform.scale(bg2_image, (bg2_image.get_width()*FACTOR_SCALE, bg2_image.get_height()*FACTOR_SCALE))
image3 = pygame.transform.scale(bg3_image, (bg3_image.get_width()*FACTOR_SCALE, bg3_image.get_height()*FACTOR_SCALE))
image5 = pygame.transform.scale(bg5_image, (bg5_image.get_width()*FACTOR_SCALE, bg5_image.get_height()*FACTOR_SCALE))

image4 = pygame.transform.scale(bg4_image, (bg4_image.get_width()*FACTOR_SCALE, bg4_image.get_height()*FACTOR_SCALE))
image4_x = -20
image4_return = False

cloud = pygame.transform.scale(single_cloud_image, (single_cloud_image.get_width()*2, single_cloud_image.get_height()*2))
cloud_x = 0

mixer.music.play()
img3_x = 0
clouds_x = 0
clouds_y = 0
main_text = "Si tengo apetito es solo..."
main_text_french = "Si j???ai du go??t, ce n???est gu??re..."

main_font_french = pygame.font.SysFont('Verdana', 50)
main_font = pygame.font.SysFont('Verdana', 20)

run = True
while run:
    # paint background
    display.fill((146,244,255))

    #   scroll and camera offset
    true_scroll[0] += (player_rect.x-true_scroll[0]-300)/5
    true_scroll[1] += (player_rect.y-true_scroll[1]-290)/5
    #   purify scroll integers 
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    #   draw background
    display.blit(image, (0, 0))
    display.blit(image2, (0, 0))
    display.blit(image3, (clouds_x, clouds_y))
    
    #   create and render background poem
    main_text_french_render = main_font_french.render(main_text_french, True, (255,0,0))
    main_text_render = main_font.render(main_text, True, (0,0,0))
    main_text_render.set_alpha(125)
    
    # display.blit(main_text_french_render, (100, 100))
    display.blit(main_text_render, (200, 100))


    display.blit(image5, (clouds_x, clouds_y))

    #   lullaby clouds animation
    display.blit(cloud, (clouds_x, clouds_y))
    display.blit(image4, (clouds_x*3, clouds_y*3))
    
    if not image4_return:
        image4_x += 1
        clouds_x += 0.03
        if image4_x > -1:
            image4_return = True
    else:
        image4_x -= 1
        clouds_x -= 0.03
        if image4_x < -50:
            image4_return = False


    #   text poem logic
    if player_rect.x < 500:
        main_text = "Si tengo apetito es solo..."
        # letter = list(text).pop()
        # main_text += main_text + list(text).pop()
    if player_rect.x > 500 and player_rect.x < 1000:
        main_text = "...de la tierra y de las piedras"
    if player_rect.x > 1000 and player_rect.x < 1500:
        main_text = "Almuerzo siempre con aire..."
    if player_rect.x > 1500 and player_rect.x < 2000:
        main_text = "...tierra, carbones y piedras"



    tile_rects = []

    #   display tiles and things and 
    y = 0
    for row in game_map:
        x = 0
        for tile in row:
            if tile == '1':
                display.blit(ground_image_resized, (x * TILE_SIZE_SCALE-scroll[0], y * TILE_SIZE_SCALE-scroll[1]))
            if tile == '2':
                display.blit(shopp, (x * TILE_SIZE-scroll[0], y * TILE_SIZE-scroll[1]))
            if tile not in ['0', '2']:
                tile_rects.append(pygame.Rect(x * TILE_SIZE_SCALE, y * TILE_SIZE_SCALE, TILE_SIZE_SCALE, TILE_SIZE_SCALE))
            x += 1
        y += 1



    player_movement = [0,0]
    if moving_right and not moving_down:
        # clouds_x += 0.03
        player_movement[0] += PLAYER_MOVEMENT_SPEED
    if moving_left and not moving_down:
        # clouds_x -= 0.03
        player_movement[0] -= PLAYER_MOVEMENT_SPEED
    if moving_up:
        clouds_y += 0.03
        # print('moving up')
        # player_movement[1] += PLAYER_MOVEMENT_SPEED
    if moving_down:
        # print('moving down')
        clouds_y -= 0.03
        # player_movement[1] -= PLAYER_MOVEMENT_SPEED
        

    player_movement[1] += player_y_momentum
    player_y_momentum += velocity

    if player_y_momentum > 10:
        player_y_momentum = 10

    if player_movement[0] > 0:
        player_action, player_frame = change_action(player_action, player_frame, 'walk')
        img3_x += 0.01
        player_flip = False
    if player_movement[0] < 0:
        player_action, player_frame = change_action(player_action, player_frame, 'walk')
        player_flip = True
    #   IDLE
    if player_movement[0] == 0:
        player_action, player_frame = change_action(player_action, player_frame, 'sitting-idle')
        # player_flip = False
    if moving_down and not moving_left:
        player_action, player_frame = change_action(player_action, player_frame, 'munch')
    if moving_down and moving_left:
        player_action, player_frame = change_action(player_action, player_frame, 'munch')
        player_flip = True


    player_rect, collisions = move(player_rect, player_movement, tile_rects)
    # print("player X "+str(player_rect.x))
    if collisions['bottom']:
        player_is_jumping = False
        player_y_momentum = 0

    #   draw player sprite
    player_frame += 1
    if player_frame >= len(animation_database[player_action]):
        player_frame = 0
    player_img_id = animation_database[player_action][player_frame]
    player_img = animation_frames[player_img_id]

    display.blit(pygame.transform.flip(player_img, player_flip, False), (player_rect.x-scroll[0], player_rect.y-scroll[1]))


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
            if event.key == K_UP:
                moving_up = True
                player_is_jumping = True
                player_y_momentum = -5
            if event.key == K_DOWN:
                moving_down = True
                player_is_jumping = False
                player_y_momentum = 5
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                moving_right = False
            if event.key == K_LEFT:
                moving_left = False
            if event.key == K_UP:
                moving_up = False
            if event.key == K_DOWN:
                moving_down = False
            
    
    # screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0,0))
    screen.blit(display, (0,0))
    pygame.display.update()
    clock.tick(60)
    # print(clock.get_fps())