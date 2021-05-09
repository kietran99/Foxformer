import pygame
from random import randint

from utils import foreach
from global_path import *






TILE_SIZE = pygame.image.load(env_root + 'grass_0.png').get_width()
DIRT_VAR = '1'
NONE = '0'
BG_LEN = 4
BG_MOVE_MODIFIER = 0.25
CAMERA_SMOOTH_FACTOR = 10

def load_map(path):
	f = open(path + '.txt', 'r')
	data = f.read()
	f.close()
	data = data.split('\n')
	return [list(map(lambda tile: dirt_codes[randint(0, len(dirt_codes) - 1)] if tile == DIRT_VAR else tile, list(row))) for row in data]

def collision_test(rect, tiles):
	return [tile for tile in tiles if rect.colliderect(tile)]

def render_bg(display, scroll):
	foreach(lambda i: display.blit(bg_img, ((i - 1) * bg_img.get_width() - scroll[0] * BG_MOVE_MODIFIER, 0)), range(BG_LEN + 1))

def render_map(game_map, display, scroll):
	tile_rects = []
	y = 0
	for row in game_map:
		x = 0
		for tile in row:
			pos = (x * TILE_SIZE, y * TILE_SIZE)
			scrolledPos = (pos[0] - scroll[0], pos[1] - scroll[1])
			
			if tile in tile_dict:
				display.blit(tile_dict[tile], scrolledPos)	

				if tile != NONE:
					tile_rects.append(pygame.Rect(pos[0], pos[1], TILE_SIZE, TILE_SIZE))

			x += 1

		y += 1

	return tile_rects

def merge_maps(map_0, map_1):
	return [a + b for a, b in zip(map_0, map_1)]

def calc_scroll(display, player):
	player.true_scroll[0] += (player.rect.x - player.true_scroll[0] - display.get_width() / 2 + player.rect.width / 2) / CAMERA_SMOOTH_FACTOR
	player.true_scroll[1] += (player.rect.y - player.true_scroll[1] - display.get_height() / 2 + player.rect.height / 2) / CAMERA_SMOOTH_FACTOR
	player.true_scroll[1] = player.true_scroll[1] if player.true_scroll[1] <= 112 else 112
	scroll = player.true_scroll.copy()
	scroll[0] = int(scroll[0])
	scroll[1] = int(scroll[1])

	return player.true_scroll, scroll

dirt_codes = ['1', '3', '4']

tile_dict = {
	'1': pygame.image.load(env_root + 'dirt_main.png'),
	'3': pygame.image.load(env_root + 'dirt_0.png'),
	'4': pygame.image.load(env_root + 'dirt_1.png'),
	'2': pygame.image.load(env_root + 'grass_0.png')
}

bg_img = pygame.image.load(env_root + 'back.png')