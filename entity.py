import pygame

from global_path import *

from map import TILE_SIZE
from enemy import *
from item import *






enemies_dict = {
	'2': lambda pos: Opossum((pos[0] - 0, pos[1] - OPOSSUM_Y))
}

items_dict = {
	'5': lambda pos: Cherry((pos[0], pos[1] - CHERRY_Y))
}

def gen_entities(entities_map, display, scroll):
	enemies = []
	items = []

	y = 0
	for row in entities_map:
		x = 0
		for entity in row:
			pos = (x * TILE_SIZE, y * TILE_SIZE)
			scrolledPos = (pos[0] - scroll[0], pos[1] - scroll[1])
			
			if entity in enemies_dict:
				enemies.append(enemies_dict[entity](scrolledPos))

			elif entity in items_dict:
				items.append(items_dict[entity](scrolledPos))

			x += 1

		y += 1

	return enemies, items