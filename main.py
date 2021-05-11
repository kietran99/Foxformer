import pygame, sys
from functools import reduce

from global_path import *
from config import *
from utils import foreach
from event_channel import remove_all_listeners

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
	# load_map('maps/map_0'), 
	# load_map('maps/map_1'),
	# load_map('maps/map_2'),
	load_map('maps/map_3'),
	load_map('maps/map_4')
]

game_map = reduce(merge_maps, map_pieces)

entity_pieces = [
	# load_entity_map('maps/entities_0'),
	# load_entity_map('maps/entities_1'),
	# load_entity_map('maps/entities_2'),
	load_entity_map('maps/entities_3'),
	load_entity_map('maps/entities_4')
]

entities_map = reduce(merge_maps, entity_pieces)

def spawn_boss(_):
	global enemies, boss
	enemies.append(boss)

def reset_game():
	remove_all_listeners()
	add_listener("Boss Zone Entered", spawn_boss)
	game_manager = GameManager()
	player = Player()
	enemies, boss, items = gen_entities(entities_map, display, calc_scroll(display, player)[1])
	UI = UICanvas()
	vfxManager = VFXManager()
	return game_manager, player, enemies, boss, items, UI, vfxManager

game_manager, player, enemies, boss, items, UI, vfxManager = reset_game()

pygame.mixer.music.load('audio/bgm.ogg')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.0)



while True:
	display.fill((146, 244, 255))

	if player.rect.y > MAP_BOTTOM:
		game_manager, player, enemies, boss, items, UI, vfxManager = reset_game()
		continue

	player.true_scroll, scroll = calc_scroll(display, player)

	bind_render_input = lambda render_fn: render_fn(display, scroll)
	bind_render_input(render_bg)
	tile_rects = render_map(game_map, display, scroll)

	player.try_move(tile_rects)

	dead_enemies, killed_player = enemies_update(enemies, tile_rects, player.rect, display, scroll)

	if killed_player:
		game_manager, player, enemies, boss, items, UI, vfxManager = reset_game()
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
	clock.tick(FPS)

