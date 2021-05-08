import pygame, sys
from functools import reduce

from global_path import *
from config import *
from utils import foreach

from game_manager import GameManager
from animation import *
from map import *
from player import *
from entity import *
from UI import *
from vfx import VFXManager





clock = pygame.time.Clock()

from pygame.locals import *

pygame.init()
pygame.display.set_caption('Foxformer')
window = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
display = pygame.Surface((WINDOW_SIZE[0] / RESOLUTION, WINDOW_SIZE[1] / RESOLUTION))

map_pieces = [
	load_map('maps/map_0'), 
	load_map('maps/map_1')
]

game_map = reduce(merge_maps, map_pieces)

entity_pieces = [
	load_entity_map('maps/entities_0'),
	load_entity_map('maps/entities_1')
]

entities_map = reduce(merge_maps, entity_pieces)

def reset_game():
	game_manager = GameManager()
	player = Player()
	enemies, items = gen_entities(entities_map, display, calc_scroll(display, player, player.true_scroll)[1])
	UI = UICanvas()
	return game_manager, player, enemies, items, UI

game_manager, player, enemies, items, UI = reset_game()

vfxManager = VFXManager()

pygame.mixer.music.load('audio/bgm.ogg')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.0)

# game_over = False;

# def on_game_over(_):
# 	global game_over
# 	game_over = True

# add_listener("Game Over", on_game_over)

while True:
	display.fill((146, 244, 255))

	# if game_over:
	# 	game_manager, player, enemies, items, UI = reset_game()

	if player.rect.y > WINDOW_SIZE[1] / 1.5:
		game_manager, player, enemies, items, UI = reset_game()

	player.true_scroll, scroll = calc_scroll(display, player, player.true_scroll)

	bind_render_input = lambda render_fn: render_fn(display, scroll)
	bind_render_input(render_bg)
	tile_rects = render_map(game_map, display, scroll)

	player.try_move(tile_rects)

	dead_enemies, killed_player = enemies_update(enemies, tile_rects, player.rect, display, scroll)

	if killed_player:
		game_manager, player, enemies, items, UI = reset_game()
		continue

	foreach(lambda killed: enemies.remove(killed), dead_enemies)

	obtains = items_update(items, player.rect, display, scroll)
	foreach(lambda obtained: items.remove(obtained), obtains)

	bind_render_input(player.render)

	bind_render_input(vfxManager.render)

	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()

		player.handle_input(event)

	surface = pygame.transform.scale(display, WINDOW_SIZE)
	window.blit(surface, (0, 0))

	UI.render(window)
	
	pygame.display.update()
	clock.tick(60)

