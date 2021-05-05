import pygame, sys

from global_path import *
from config import *
from utils import foreach

from animation import *
from map import *
from player import *
from enemy import *





clock = pygame.time.Clock()

from pygame.locals import *

pygame.init()
pygame.display.set_caption('Foxformer')
window = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
display = pygame.Surface((WINDOW_SIZE[0] / RESOLUTION, WINDOW_SIZE[1] / RESOLUTION))

opossum_list = [Opossum((208, 80))]
player = Player()

def reset_game():
	player = Player()
	opossum_list = [Opossum((208, 80))]

	return player, opossum_list

while True:
	display.fill((146, 244, 255))

	player.true_scroll, scroll = calc_scroll(display, player, player.true_scroll)

	bind_render_input = lambda render_fn: render_fn(display, scroll)
	bind_render_input(render_bg)
	tile_rects = bind_render_input(render_map)

	player_movement = [0, 0]
	player_movement[0] += player.move_speed if player.moving_right else 0
	player_movement[0] -= player.move_speed if player.moving_left else 0
	player_movement[1] += player.y_momentum 
	player.y_momentum = player.y_momentum + GRAVITY_MOD if player.y_momentum <= MAX_Y_MOMENTUM else MAX_Y_MOMENTUM

	collisions = player.move(player_movement, tile_rects)
	
	if collisions['bottom']:
		player.y_momentum = 0
		player.air_timer = 0
		player.on_ground = True
	elif collisions['top']:
		player.y_momentum = 0
		player.air_timer = 0
	else:
		player.air_timer += 1

	if player_movement[0] != 0:
		player.flip = player_movement[0] < 0
		if player.on_ground:
			player.action, player.frame = change_action(player.action, player.frame, RUN)
		else:
			player.action, player.frame = change_action(player.action, player.frame, JUMP)
	else:
		player.action, player.frame = change_action(player.action, player.frame, IDLE)

	player.frame = (player.frame + 1) if player.frame < (len(animation_db[player.action]) - 1) else 0
	player_img_id = animation_db[player.action][player.frame]
	player_img = animation_frames[player_img_id]

	killed_player = False
	for opossum in opossum_list:
		opossum.move(tile_rects)
		bind_render_input(opossum.render)
		if opossum.test_player_collision(player.rect) == KILLED_PLAYER:
			player, opossum_list = reset_game()
			killed_player = True
			break

	if killed_player:
		continue

	opossum_list = [opossum for opossum in opossum_list if opossum.test_player_collision(player.rect) != GET_KILLED]

	player_pos = (player.rect.x - scroll[0] - PLAYER_SPRITE_OFFSET[0], player.rect.y - scroll[1] - PLAYER_SPRITE_OFFSET[1])
	display.blit(pygame.transform.flip(player_img, player.flip, False), player_pos)
	
	# debug_rect = pygame.Rect(player.rect.x - scroll[0], player.rect.y - scroll[1], player.rect.width, player.rect.height)
	# pygame.draw.rect(display, (255, 0, 0), debug_rect, 1)

	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()

		if event.type == KEYDOWN:
			if event.key == K_d:
				player.moving_right = True
			if event.key == K_a:
				player.moving_left = True
			if event.key == K_SPACE:
				if player.air_timer < EDGE_JUMP_TIME_LIMIT:
					player.y_momentum = -player.jump_force
					player.on_ground = False

		if event.type == KEYUP:
			if event.key == K_d:
				player.moving_right = False
			if event.key == K_a:
				player.moving_left = False

	surface = pygame.transform.scale(display, WINDOW_SIZE)
	window.blit(surface, (0, 0))
	pygame.display.update()
	clock.tick(60)

