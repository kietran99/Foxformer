from map import TILE_SIZE, NONE, load_map, tile_dict
from entity import load_entity_map

def gen_tiles_txt(map, out_path):
	tiles = ""

	y = 0
	for row in map:
		x = 0
		for tile in row:
			pos = (x * TILE_SIZE, y * TILE_SIZE)
			
			if tile in tile_dict:
				tiles += 'X'

			elif tile == NONE:
				tiles += '-'

			x += 1

		tiles += '\n'
		y += 1

	tiles = tiles[:-1]
	f = open(out_path, 'w')
	f.write(tiles)
	f.close()

def layer_tiles(entity_map, map, out_path):
	entities = ""

	y = 0
	for row in map:
		x = 0
		for tile in row:
			if tile in tile_dict:
				entities += 'X'

			elif tile == NONE:
				entities += '-' if entity_map[y][x] == '-' or entity_map[y][x] == 'X' else entity_map[y][x]

			x += 1

		entities += '\n'
		y += 1

	f = open(out_path, 'w')
	f.write(entities)
	f.close()

def gen_empty_map(out_path, height=15, width=30):
	tiles = ""

	for y in range(height):
		for x in range(width):
			tiles += '0'

		tiles += '\n'
		
	tiles = tiles[:-1]
	f = open(out_path, 'w')
	f.write(tiles)
	f.close()

# gen_tiles_txt(load_map('maps/map_2'), 'maps/entities_2.txt')
# layer_tiles(load_entity_map('maps/entities_2'), load_map('maps/map_2'), 'maps/entities_2.txt')
# gen_empty_map('maps/map_2.txt')