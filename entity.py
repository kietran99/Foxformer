import pygame

from global_path import *

from map import TILE_SIZE
from enemy import *
from item import *






enemies_dict = {
	'1': lambda pos: Opossum((pos[0] - 0, pos[1] - 5)),
	'#': lambda pos: Eagle((pos[0] - 0, pos[1] + 1), (32, 20), (0, 18))
}

items_dict = {
	'4': lambda pos: Cherry((pos[0], pos[1]), (16, 16), (2, 2)),
	'6': lambda pos: Spring((pos[0], pos[1] + 13), (16, 8), (0, 8)),
	'7': lambda pos: InvisTile((pos[0], pos[1] + 5), (16, 16), (0, 0)),
	'8': lambda pos: Weed((pos[0], pos[1] + 5), (16, 16), (0, 0)),
	'p': lambda pos: Pipe((pos[0], pos[1] + 5), (16, 16), (0, 0)),
	'9': lambda pos: Gem((pos[0], pos[1] + 6), (15, 13), (0, 0)),
	'/': lambda pos: BossEnterZone((pos[0], pos[1] + 4), (16, 16), (0, 0)),
}

def load_entity_map(path):
	f = open(path + '.txt', 'r')
	data = f.read()
	f.close()
	data = data.split('\n')
	return [list(row) for row in data]

def gen_entities(entities_map, display, scroll):
	enemies = []
	boss = None
	items = []

	y = 0
	for row in entities_map:
		x = 0
		for entity in row:
			pos = (x * TILE_SIZE, y * TILE_SIZE)
			scrolledPos = (pos[0] - scroll[0], pos[1] - scroll[1])
			
			if entity in enemies_dict:
				if entity == '#':
					boss = enemies_dict[entity](scrolledPos)
				else:
					enemies.append(enemies_dict[entity](scrolledPos))

			elif entity in items_dict:
				items.append(items_dict[entity](scrolledPos))

			x += 1

		y += 1

	return enemies, boss, items