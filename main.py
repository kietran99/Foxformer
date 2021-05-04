import pygame, sys
from config import *
from random import randint

clock = pygame.time.Clock()

image_root = 'images/Sunny-land-assets-files/PNG/'
sprites_root = image_root + 'sprites/'
env_root = image_root + 'environment/layers/'

from pygame.locals import *
pygame.init()

pygame.display.set_caption('Platformer')

window = pygame.display.set_mode(WINDOW_SIZE, 0, 32)

display = pygame.Surface((WINDOW_SIZE[0] / resolution, WINDOW_SIZE[1] / resolution))

player_frame = 0

global animation_frames
animation_frames = {}

def load_anim(path, frame_duration):
	global animation_frames
	animation_name = path.split('/')[-1]
	animation_frame_data = []
	n = 0
	for frame in frame_duration:
		animation_frame_id = animation_name + '_' + str(n)
		img_loc = path + '/' + animation_frame_id + '.png'
		animation_img = pygame.image.load(img_loc)
		animation_frames[animation_frame_id] = animation_img.copy()
		animation_frame_data.extend([animation_frame_id for _ in range(frame)])
		n += 1

	return animation_frame_data

def change_action(action_var, frame, new_val):
	if action_var != new_val:
		action_var = new_val
		frame = 0

	return action_var, frame

IDLE = 'idle'
RUN = 'run'
JUMP = 'jump'

animation_db = {}
animation_db[IDLE] = load_anim(sprites_root + 'player/idle', [7, 7, 7, 7])
animation_db[RUN] = load_anim(sprites_root + 'player/run', [7, 7, 7, 7, 7, 7])
animation_db[JUMP] = load_anim(sprites_root + 'player/jump', [7, 7])

player_action = IDLE
player_frame = 0
player_flip = False

grass_img = pygame.image.load(env_root + 'grass_0.png')

TILE_SIZE = grass_img.get_width()

none = '0'
dirt = '1'
grass = '2'

dirt_codes = ['1', '3', '4']

tile_dict = {
	'1': pygame.image.load(env_root + 'dirt_main.png'),
	'3': pygame.image.load(env_root + 'dirt_0.png'),
	'4': pygame.image.load(env_root + 'dirt_1.png'),
	'2': pygame.image.load(env_root + 'grass_0.png')
}

def load_map(path):
	f = open(path + '.txt', 'r')
	data = f.read()
	f.close()
	data = data.split('\n')
	return [list(map(lambda tile: dirt_codes[randint(0, len(dirt_codes) - 1)] if tile == dirt else tile, list(row))) for row in data]

game_map = load_map('maps/map')

bg_img = pygame.image.load(env_root + 'back.png')

def collision_test(rect, tiles):
	return [tile for tile in tiles if rect.colliderect(tile)]

def move(rect, movement, tiles):
	collision_types = { 'top': False, 'bottom': False, 'right': False, 'left': False }

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

player_y_momentum = 0
air_timer = 0

player_rect = pygame.Rect(100, 100, player_width, player_height)

true_scroll = [0, 0]
on_ground = True

while True:
	display.fill((146, 244, 255))

	true_scroll[0] += (player_rect.x - true_scroll[0] - display.get_width() / 2 + player_rect.width / 2) / camera_smooth_factor
	true_scroll[1] += (player_rect.y - true_scroll[1] - display.get_height() / 2 + player_rect.height / 2) / camera_smooth_factor
	scroll = true_scroll.copy()
	scroll[0] = int(scroll[0])
	scroll[1] = int(scroll[1])

	for i in range(bg_len + 1):
		display.blit(bg_img, ((i - 1) * bg_img.get_width() - scroll[0] * bg_move_modifier, 0))

	tile_rects = []
	y = 0
	for row in game_map:
		x = 0
		for tile in row:
			pos = (x * TILE_SIZE, y * TILE_SIZE)
			scrolledPos = (pos[0] - scroll[0], pos[1] - scroll[1])
			
			if tile in tile_dict:
				display.blit(tile_dict[tile], scrolledPos)	

			if tile != none:
				tile_rects.append(pygame.Rect(pos[0], pos[1], TILE_SIZE, TILE_SIZE))

			x += 1

		y += 1	

	player_movement = [0, 0]
	player_movement[0] += move_speed if moving_right else 0
	player_movement[0] -= move_speed if moving_left else 0
	player_movement[1] += player_y_momentum 
	player_y_momentum = player_y_momentum + gravity_modifier if player_y_momentum <= max_y_momentum else max_y_momentum

	player_rect, collisions = move(player_rect, player_movement, tile_rects)
	
	if collisions['bottom']:
		player_y_momentum = 0
		air_timer = 0
		on_ground = True
	else:
		air_timer += 1

	if player_movement[0] != 0:
		player_flip = player_movement[0] < 0
		if on_ground:
			player_action, player_frame = change_action(player_action, player_frame, RUN)
		else:
			player_action, player_frame = change_action(player_action, player_frame, JUMP)
	else:
		player_action, player_frame = change_action(player_action, player_frame, IDLE)

	player_frame = (player_frame + 1) if player_frame < (len(animation_db[player_action]) - 1) else 0
	player_img_id = animation_db[player_action][player_frame]
	player_img = animation_frames[player_img_id]

	display.blit(pygame.transform.flip(player_img, player_flip, False), (player_rect.x - scroll[0], player_rect.y - scroll[1]))

	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()

		if event.type == KEYDOWN:
			if event.key == K_d:
				moving_right = True
			if event.key == K_a:
				moving_left = True
			if event.key == K_SPACE:
				if air_timer < edge_jump_time_limit:
					player_y_momentum = -jump_force
					on_ground = False

		if event.type == KEYUP:
			if event.key == K_d:
				moving_right = False
			if event.key == K_a:
				moving_left = False

	surface = pygame.transform.scale(display, WINDOW_SIZE)
	window.blit(surface, (0, 0))
	pygame.display.update()
	clock.tick(60)

