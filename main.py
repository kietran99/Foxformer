import pygame, sys

from global_path import *
from config import *
from utils import foreach

from game_manager import GameManager
from animation import *
from map import *
from player import *
from entity import *
from UI import *





clock = pygame.time.Clock()

from pygame.locals import *

pygame.init()
pygame.display.set_caption('Foxformer')
window = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
display = pygame.Surface((WINDOW_SIZE[0] / RESOLUTION, WINDOW_SIZE[1] / RESOLUTION))

# gen_tiles_txt(game_map, 'maps/tiles.txt')
entities_map = load_map('maps/entities')

def reset_game():
	game_manager = GameManager()
	player = Player()
	enemies, items = gen_entities(entities_map, display, calc_scroll(display, player, player.true_scroll)[1])
	UI = UICanvas()
	return game_manager, player, enemies, items, UI

game_manager, player, enemies, items, UI = reset_game()

pygame.mixer.music.load('audio/bgm.ogg')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.5)

while True:
	display.fill((146, 244, 255))

	player.true_scroll, scroll = calc_scroll(display, player, player.true_scroll)

	bind_render_input = lambda render_fn: render_fn(display, scroll)
	bind_render_input(render_bg)
	tile_rects = bind_render_input(render_map)

	player.try_move(tile_rects)

	dead_enemies, killed_player = enemies_update(enemies, tile_rects, player.rect, display, scroll)

	if killed_player:
		game_manager, player, enemies, items, UI = reset_game()
		continue

	foreach(lambda killed: enemies.remove(killed), dead_enemies)

	obtains = items_update(items, player.rect, display, scroll)
	foreach(lambda obtained: items.remove(obtained), obtains)

	bind_render_input(player.render)

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

