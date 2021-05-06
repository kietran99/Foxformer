import pygame
from random import randint

from utils import foreach
from global_path import *






TILE_SIZE = pygame.image.load(env_root + 'grass_0.png').get_width()
DIRT_VAR = '1'
NONE = '0'
BG_LEN = 4
BG_MOVE_MODIFIER = 0.25

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

def render_map(display, scroll):
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

dirt_codes = ['1', '3', '4']

tile_dict = {
	'1': pygame.image.load(env_root + 'dirt_main.png'),
	'3': pygame.image.load(env_root + 'dirt_0.png'),
	'4': pygame.image.load(env_root + 'dirt_1.png'),
	'2': pygame.image.load(env_root + 'grass_0.png')
}

game_map = load_map('maps/map')
bg_img = pygame.image.load(env_root + 'back.png')