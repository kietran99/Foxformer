import pygame

from global_path import *

from map import *
from enemy import enemies_dict
from item import items_dict






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