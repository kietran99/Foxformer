import pygame
from pygame.locals import *

from config import *
from global_path import *
from event_channel import add_listener

from map import *
from animation import *






PLAYER_WIDTH = 16
PLAYER_HEIGHT = 22
PLAYER_SPRITE_OFFSET = (8, 10)
EDGE_JUMP_TIME_LIMIT = 15
GRAVITY_MOD = 0.2
MAX_Y_MOMENTUM = 3

class Player:
	def __init__(self):
		self.move_speed = 3
		self.jump_force = 4

		self.moving_right = False
		self.moving_left = False

		self.y_momentum = 0
		self.air_timer = 0

		self.rect = pygame.Rect(144, 144, PLAYER_WIDTH, PLAYER_HEIGHT)

		self.on_ground = True

		self.true_scroll = [0, 0]

		self.action = IDLE
		self.frame = 0
		self.flip = False

		self.sprite = None

		self.double_jump_enabled = False
		self.is_second_jump = False

		self.dash_enabled = False
		self.dash_speed = 8
		self.dash_time = 0.1
		self.elapsed_dash_time = 0.0

		add_listener("Enemy Killed", lambda _: self.jump(4))
		add_listener("On Spring Collide", lambda _: self.jump(7))
		add_listener("On Crate Broken", lambda _: self.jump(4))
		add_listener("On Weed Obtained", lambda _: self.enable_double_jump())
		add_listener("On Pipe Obtained", lambda _: self.enable_dash())
		add_listener("Boss Damaged", lambda _: self.jump(4))

	def handle_input(self, event):
		if event.type == KEYDOWN:
			if event.key == K_d:
				self.moving_right = True
			if event.key == K_a:
				self.moving_left = True
			if event.key == K_SPACE:
				self.try_jump()
			if self.dash_enabled and not self.is_second_jump and event.key == K_LSHIFT and not self.on_ground:
				self.dash()

		if event.type == KEYUP:
			if event.key == K_d:
				self.moving_right = False
			if event.key == K_a:
				self.moving_left = False

	def try_move(self, tile_rects):
		player_movement = [0, 0]

		if self.elapsed_dash_time > 0.0:
			player_movement[0] += self.dash_speed if self.moving_right else 0
			player_movement[0] -= self.dash_speed if self.moving_left else 0
			self.elapsed_dash_time -= DELTA
		else:
			player_movement[0] += self.move_speed if self.moving_right else 0
			player_movement[0] -= self.move_speed if self.moving_left else 0
			player_movement[1] += self.y_momentum
			self.y_momentum = self.y_momentum + GRAVITY_MOD if self.y_momentum <= MAX_Y_MOMENTUM else MAX_Y_MOMENTUM

		collisions = self.move(player_movement, tile_rects)
		
		if collisions['bottom']:
			self.y_momentum = 0
			self.air_timer = 0
			self.on_ground = True
			self.is_second_jump = False
		elif collisions['top']:
			self.y_momentum = 0
			self.air_timer = 0
		else:
			self.air_timer += 1

		if not self.on_ground:
			self.flip = player_movement[0] < 0
			self.action, self.frame = change_action(self.action, self.frame, JUMP if self.elapsed_dash_time <= 0.0 else DASH)
		else:
			if player_movement[0] != 0:
				self.flip = player_movement[0] < 0
				self.action, self.frame = change_action(self.action, self.frame, RUN)
			else:
				self.action, self.frame = change_action(self.action, self.frame, IDLE)		

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
		if not self.on_ground:
			if not self.double_jump_enabled:
				return

			if self.is_second_jump:
				return

			self.is_second_jump = True
			self.jump(self.jump_force)

		if self.air_timer < EDGE_JUMP_TIME_LIMIT:
			self.jump()

	def jump(self, jump_force=None):
		self.y_momentum = -jump_force if jump_force != None else -self.jump_force
		self.on_ground = False

	def enable_double_jump(self):
		self.double_jump_enabled = True

	def enable_dash(self):
		self.dash_enabled = True

	def dash(self):
		self.elapsed_dash_time = self.dash_time

	def render(self, display, scroll):
		# debug_rect = pygame.Rect(self.rect.x - scroll[0], self.rect.y - scroll[1], self.rect.width, self.rect.height)
		# pygame.draw.rect(display, (255, 0, 0), debug_rect, 1)

		self.frame = (self.frame + 1) if self.frame < (len(animation_db[self.action]) - 1) else 0
		player_img_id = animation_db[self.action][self.frame]
		self.sprite = animation_frames[player_img_id]
		player_pos = (self.rect.x - scroll[0] - PLAYER_SPRITE_OFFSET[0], self.rect.y - scroll[1] - PLAYER_SPRITE_OFFSET[1])
		display.blit(pygame.transform.flip(self.sprite, self.flip, False), player_pos)

IDLE = 'idle'
RUN = 'run'
JUMP = 'jump'
DASH = 'dash'

animation_db = {}
animation_db[IDLE] = load_anim(sprites_root + 'player/idle', [7, 7, 7, 7])
animation_db[RUN] = load_anim(sprites_root + 'player/run', [5, 5, 5, 5, 5, 5])
animation_db[JUMP] = load_anim(sprites_root + 'player/jump', [7])
animation_db[DASH] = load_anim(sprites_root + 'player/dash', [5, 5])

