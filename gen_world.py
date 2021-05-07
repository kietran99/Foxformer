from map import gen_tiles_txt, load_map
from entity import layer_tiles, load_entity_map

# gen_tiles_txt(load_map('maps/map_1'), 'maps/entities_1.txt')
layer_tiles(load_entity_map('maps/entities_1'), load_map('maps/map_1'), 'maps/entities_1.txt')