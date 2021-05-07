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
		self.move_speed = 3
		self.jump_force = 3.5

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

		self.sprite = None

	def try_move(self, tile_rects):
		player_movement = [0, 0]
		player_movement[0] += self.move_speed if self.moving_right else 0
		player_movement[0] -= self.move_speed if self.moving_left else 0
		player_movement[1] += self.y_momentum 
		self.y_momentum = self.y_momentum + GRAVITY_MOD if self.y_momentum <= MAX_Y_MOMENTUM else MAX_Y_MOMENTUM

		collisions = self.move(player_movement, tile_rects)
		
		if collisions['bottom']:
			self.y_momentum = 0
			self.air_timer = 0
			self.on_ground = True
		elif collisions['top']:
			self.y_momentum = 0
			self.air_timer = 0
		else:
			self.air_timer += 1

		if player_movement[0] != 0:
			self.flip = player_movement[0] < 0
			if self.on_ground:
				self.action, self.frame = change_action(self.action, self.frame, RUN)
			else:
				self.action, self.frame = change_action(self.action, self.frame, JUMP)
		else:
			self.action, self.frame = change_action(self.action, self.frame, IDLE)

		self.frame = (self.frame + 1) if self.frame < (len(animation_db[self.action]) - 1) else 0
		player_img_id = animation_db[self.action][self.frame]
		self.sprite = animation_frames[player_img_id]

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

	def try_jump(self):
		if self.air_timer < EDGE_JUMP_TIME_LIMIT:
			self.y_momentum = -self.jump_force
			self.on_ground = False

	def render(self, display, scroll):
		# debug_rect = pygame.Rect(player.rect.x - scroll[0], player.rect.y - scroll[1], player.rect.width, player.rect.height)
		# pygame.draw.rect(display, (255, 0, 0), debug_rect, 1)
		player_pos = (self.rect.x - scroll[0] - PLAYER_SPRITE_OFFSET[0], self.rect.y - scroll[1] - PLAYER_SPRITE_OFFSET[1])
		display.blit(pygame.transform.flip(self.sprite, self.flip, False), player_pos)

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

