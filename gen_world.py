from functools import reduce

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
	f = open(out_path + '.txt', 'w')
	f.write(tiles)
	f.close()

def layer_tiles(map, out_path):
	entity_map = load_entity_map(out_path)
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

	f = open(out_path + '.txt', 'w')
	f.write(entities)
	f.close()

def gen_empty_map(out_path, height=15, width=30):
	tiles = ""

	for y in range(height):
		for x in range(width):
			tiles += '0'

		tiles += '\n'
		
	tiles = tiles[:-1]
	f = open(out_path + '.txt', 'w')
	f.write(tiles)
	f.close()

def gen_new_row(path, fill_char):
	f = open(path + '.txt', 'r')
	data = f.read()
	row_len = len(data.split('\n')[0])
	new_row = reduce(lambda s1, s2: s1 + fill_char, range(row_len), '')
	new_row += '\n'
	f.close()
	return new_row

def append_top_map(fill_char, path_format, n_maps, n_rows):
	new_row = gen_new_row(path_format + '_0', fill_char)

	for i in range(n_maps):
		f = open(path_format + '_' + str(i) + '.txt', 'r')
		data = f.read()
		new_rows = reduce(lambda s1, s2: s1 + new_row, range(n_rows), '')
		new_data = new_rows + data
		f.close()

		f = open(path_format + '_' + str(i) + '.txt', 'w')
		f.write(new_data)
		f.close()

# gen_tiles_txt(load_map('maps/map_3'), 'maps/entities_3')
# layer_tiles(load_map('maps/map_0'), 'maps/entities_0')
# gen_empty_map('maps/map_3')
# append_top_map('0', 'maps/map', 4, 1)
# append_top_map('-', 'maps/entities', 4, 1)