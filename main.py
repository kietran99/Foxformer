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

pygame.mixer.music.load('audio/bgm.ogg')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.0)

class MainGame:
	def __init__(self, window, display):
		self.window = window
		self.display = display

		map_pieces = [
			load_map('maps/map_0'), 
			load_map('maps/map_1'),
			load_map('maps/map_2'),
			load_map('maps/map_3'),
			load_map('maps/map_4')
		]

		self.game_map = reduce(merge_maps, map_pieces)

		entity_pieces = [
			load_entity_map('maps/entities_0'),
			load_entity_map('maps/entities_1'),
			load_entity_map('maps/entities_2'),
			load_entity_map('maps/entities_3'),
			load_entity_map('maps/entities_4')
		]

		self.entities_map = reduce(merge_maps, entity_pieces)

		self.reset_game()
		self.is_in_game = False

	def reset_game(self):
		remove_all_listeners()
		add_listener("Boss Zone Entered", self.spawn_boss)
		add_listener("New Game", self.new_game)
		add_listener("Exit Game", self.exit_game)
		self.game_manager = GameManager()
		self.player = Player()
		self.enemies, self.boss, self.items = gen_entities(self.entities_map, self.display, calc_scroll(self.display, self.player)[1])
		self.UI = UICanvas()
		self.vfxManager = VFXManager()
		self.main_menu = MainMenu(display)

	def spawn_boss(self, _):
		self.enemies.append(self.boss)

	def new_game(self, _):
		self.is_in_game = True

	def exit_game(self, _):
		pygame.quit()
		sys.exit()

	def game_loop(self):
		while True:
			self.display.fill((146, 244, 255))

			if not self.is_in_game:
				for event in pygame.event.get():
					if event.type == QUIT:
						pygame.quit()
						sys.exit()

					self.main_menu.handle_input(event)

				surface = pygame.transform.scale(self.display, WINDOW_SIZE)
				self.window.blit(surface, (0, 0))
				
				self.main_menu.render(window)

				pygame.display.update()
				clock.tick(FPS)

				continue

			if self.player.rect.y > MAP_BOTTOM:
				self.reset_game()
				continue

			self.player.true_scroll, scroll = calc_scroll(self.display, self.player)

			bind_render_input = lambda render_fn: render_fn(self.display, scroll)
			bind_render_input(render_bg)
			tile_rects = render_map(self.game_map, self.display, scroll)

			self.player.try_move(tile_rects)

			dead_enemies, killed_player = enemies_update(self.enemies, tile_rects, self.player.rect, self.display, scroll)

			if killed_player:
				self.reset_game()
				continue

			foreach(lambda killed: self.enemies.remove(killed), dead_enemies)

			obtains = items_update(self.items, self.player.rect, self.display, scroll)
			foreach(lambda obtained: self.items.remove(obtained), obtains)

			bind_render_input(self.player.render)

			bind_render_input(self.vfxManager.render)

			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					sys.exit()

				self.player.handle_input(event)

			surface = pygame.transform.scale(self.display, WINDOW_SIZE)
			self.window.blit(surface, (0, 0))

			self.UI.render(self.window)
			
			pygame.display.update()
			clock.tick(FPS)

if __name__ == '__main__':
	main_game = MainGame(window, display)
	main_game.game_loop()