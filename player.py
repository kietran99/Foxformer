import pygame

from config import *
from global_path import *

from map import *
from animation import *






PLAYER_WIDTH = 21
PLAYER_HEIGHT = 22
PLAYER_SPRITE_OFFSET = (4, 10)
EDGE_JUMP_TIME_LIMIT = 15
GRAVITY_MOD = 0.2
MAX_Y_MOMENTUM = 3

class Player:
	def __init__(self):
		self.move_speed = 4
		self.jump_force = 5

		self.moving_right = False
		self.moving_left = False

		self.y_momentum = 0
		self.air_timer = 0

		self.rect = pygame.Rect(100, 100, PLAYER_WIDTH, PLAYER_HEIGHT)

		self.on_ground = True

		self.true_scroll = [0, 0]

		self.action = IDLE
		self.frame = 0
		self.flip = False

	def move(self, movement, tiles):
		collision_types = { 'top': False, 'bottom': False, 'right': False, 'left': False }

		self.rect.x += movement[0]
		hit_list = collision_test(self.rect, tiles)
		for tile in hit_list:
			if movement[0] > 0:
				self.rect.right = tile.left
				collision_types['right'] = True

			elif movement[0] < 0:
				self.rect.left = tile.right
				collision_types['left'] = True

		self.rect.y += movement[1]
		hit_list = collision_test(self.rect, tiles)
		for tile in hit_list:
			if movement[1] > 0:
				self.rect.bottom = tile.top
				collision_types['bottom'] = True
			elif movement[1] < 0:
				self.rect.top = tile.bottom
				collision_types['top'] = True

		return collision_types

def calc_scroll(display, player, true_scroll):
	player.true_scroll[0] += (player.rect.x - player.true_scroll[0] - display.get_width() / 2 + player.rect.width / 2) / camera_smooth_factor
	player.true_scroll[1] += (player.rect.y - player.true_scroll[1] - display.get_height() / 2 + player.rect.height / 2) / camera_smooth_factor
	scroll = player.true_scroll.copy()
	scroll[0] = int(scroll[0])
	scroll[1] = int(scroll[1])

	return true_scroll, scroll

IDLE = 'idle'
RUN = 'run'
JUMP = 'jump'

animation_db = {}
animation_db[IDLE] = load_anim(sprites_root + 'player/idle', [7, 7, 7, 7])
animation_db[RUN] = load_anim(sprites_root + 'player/run', [7, 7, 7, 7, 7, 7])
animation_db[JUMP] = load_anim(sprites_root + 'player/jump', [7, 7])

