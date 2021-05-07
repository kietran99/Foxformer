import pygame, sys

from global_path import *
from config import *
from utils import foreach

from animation import *
from map import *
from player import *
from entity import *
from enemy import *
from item import *





clock = pygame.time.Clock()

from pygame.locals import *

pygame.init()
pygame.display.set_caption('Foxformer')
window = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
display = pygame.Surface((WINDOW_SIZE[0] / RESOLUTION, WINDOW_SIZE[1] / RESOLUTION))

entities_map = load_map('maps/entities')

def reset_game():
	player = Player()
	enemies, items = gen_entities(entities_map, display, calc_scroll(display, player, player.true_scroll)[1])
	return player, enemies, items

player, enemies, items = reset_game()

pygame.mixer.music.load('audio/bgm.ogg')
pygame.mixer.music.play(-1)

while True:
	display.fill((146, 244, 255))

	player.true_scroll, scroll = calc_scroll(display, player, player.true_scroll)

	bind_render_input = lambda render_fn: render_fn(display, scroll)
	bind_render_input(render_bg)
	tile_rects = bind_render_input(render_map)

	player.try_move(tile_rects)

	dead_enemies, killed_player = enemies_update(enemies, tile_rects, player.rect, display, scroll)

	if killed_player:
		player, enemies, items = reset_game()
		continue

	if dead_enemies:
		player.y_momentum = -player.jump_force
		player.on_ground = False

	foreach(lambda killed: enemies.remove(killed), dead_enemies)

	obtains = items_update(items, player.rect, display, scroll)
	foreach(lambda obtained: items.remove(obtained), obtains)

	bind_render_input(player.render)

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
				player.try_jump()

		if event.type == KEYUP:
			if event.key == K_d:
				player.moving_right = False
			if event.key == K_a:
				player.moving_left = False

	surface = pygame.transform.scale(display, WINDOW_SIZE)
	window.blit(surface, (0, 0))
	pygame.display.update()
	clock.tick(60)

