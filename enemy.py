import pygame
from math import sqrt

from global_path import *
from config import DELTA
from animation import *
from event_channel import trigger

from map import *




OPOSSUM_WIDTH = 35
OPOSSUM_HEIGHT = 24
OPOSSUM_SPRITE_OFFSET = (0, 2)

PLAYER_DMG_TOP_OFFSET = 27

NONE = 0
KILLED_PLAYER = 1
GET_KILLED = 2



def enemies_update(enemies, tile_rects, player_rect, is_dashing, display, scroll):
	killed_player = False
	dead_enemies = []

	for enemy in enemies:
		enemy.update(tile_rects)
		collision_res = enemy.test_player_collision(player_rect, is_dashing)
		if collision_res == KILLED_PLAYER:
			# trigger("Game Over", 0)	
			killed_player = True
			break

		elif collision_res == GET_KILLED:
			dead_enemies.append(enemy)

		enemy.render(display, scroll)

	return dead_enemies, killed_player

class Opossum:
	def __init__(self, pos):
		self.move_speed = 2
		self.move_dir_mult = 1
		self.rect = pygame.Rect(pos[0], pos[1], OPOSSUM_WIDTH, OPOSSUM_HEIGHT)
		self.flip = False
		self.action = 'RUN'
		self.frame = 0

	def update(self, tiles):
		self.rect.x += self.move_speed * self.move_dir_mult

		if collision_test(self.rect, tiles):
			self.move_dir_mult *= -1

		ground_check_rect = self.rect.copy()
		ground_check_rect.x += OPOSSUM_WIDTH
		ground_check_rect.y += 10
		if not collision_test(ground_check_rect, tiles):
			self.move_dir_mult *= -1
			return

		ground_check_rect.x -= 2 * OPOSSUM_WIDTH
		if not collision_test(ground_check_rect, tiles):
			self.move_dir_mult *= -1

	def test_player_collision(self, player_rect, is_dashing):
		if not self.rect.colliderect(player_rect):
			return NONE

		cropped_rect = self.rect.clip(player_rect)
		killed_player = cropped_rect.width < cropped_rect.height and not is_dashing
			
		if not killed_player:
			trigger("Enemy Killed", (self.rect.x, self.rect.y))

		return KILLED_PLAYER if killed_player else GET_KILLED

	def render(self, display, scroll):
		# debug_rect = pygame.Rect(self.rect.x - scroll[0], self.rect.y - scroll[1], self.rect.width, self.rect.height)
		# pygame.draw.rect(display, (255, 0, 0), debug_rect, 1)
		self.flip = self.move_dir_mult > 0
		self.frame = (self.frame + 1) if self.frame < (len(opossum_anim_db[self.action]) - 1) else 0
		img_id = opossum_anim_db[self.action][self.frame]
		sprite = animation_frames[img_id]
		display.blit(pygame.transform.flip(sprite, self.flip, False), (self.rect.x - scroll[0] - OPOSSUM_SPRITE_OFFSET[0], self.rect.y - scroll[1] - OPOSSUM_SPRITE_OFFSET[1]))

class Eagle:
	def __init__(self, pos, size, sprite_offset):
		self.move_speed = 2
		self.move_dir_mult = -1
		self.hp = 3
		self.rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
		self.dmg_cooldown = 3
		self.elapsed_dmg_cooldown = 0.0
		self.original_height = pos[1]

		self.atk_charge_time = 1.0
		self.elapsed_atk_charge_time = 0.0
		self.charge_y_speed = 0.1

		self.atk_speed = 4
		self.atk_target = None
		self.atk_cooldown = 5.0
		self.elapsed_atk_cooldown = 5.0
		self.locked_target = False

		self.is_flying_back = False
		self.flying_back_speed = 1.5

		self.sprite_offset = sprite_offset
		self.flip = False
		self.action = 'FLY'
		self.frame = 0
		self.anim_db = {}
		self.anim_db['FLY'] = load_anim(sprites_root + 'eagle/attack', [7, 7, 7, 7])
		self.anim_db['DAMAGED'] = load_anim(sprites_root + 'eagle/damaged', [20])

	def update(self, tiles):
		if self.elapsed_atk_cooldown <= 0:
			if self.elapsed_atk_charge_time > 0:
				self.elapsed_atk_charge_time -= DELTA
				self.rect.y -= self.charge_y_speed
				return

			atk_dir = (self.atk_target.x - self.rect.x, self.atk_target.y - self.rect.y)
			atk_len = sqrt(atk_dir[0] ** 2 + atk_dir[1] ** 2)
			normalized_atk_dir = (atk_dir[0] / atk_len, atk_dir[1] / atk_len)
			self.rect.x += normalized_atk_dir[0] * self.atk_speed
			self.rect.y += normalized_atk_dir[1] * self.atk_speed

			if self.rect.colliderect(self.atk_target):
				self.elapsed_atk_cooldown = self.atk_cooldown
				self.is_flying_back = True
				self.locked_target = False
				self.atk_target = None
				return

			return

		if self.is_flying_back and self.rect.y > self.original_height:
			self.rect.y -= self.flying_back_speed

		self.rect.x += self.move_speed * self.move_dir_mult

		if collision_test(self.rect, tiles):
			self.move_dir_mult *= -1

		if self.elapsed_atk_cooldown > 0:
			self.elapsed_atk_cooldown -= DELTA

	def test_player_collision(self, player_rect, is_dashing):
		if self.elapsed_dmg_cooldown > 0:
			self.elapsed_dmg_cooldown -= DELTA
			return

		if not self.locked_target and self.elapsed_atk_cooldown <= 0:
			self.atk_target = pygame.Rect(player_rect.x, player_rect.bottom, 4, 1)
			self.locked_target = True
			self.elapsed_atk_charge_time = self.atk_charge_time
			if self.atk_target.x > self.rect.x:
				self.flip = True
			self.move_dir_mult = 1 if self.atk_target.x > self.rect.x else -1

		if not self.rect.colliderect(player_rect):
			return NONE

		if player_rect.bottom > self.rect.bottom and not is_dashing:
			return KILLED_PLAYER

		cropped_rect = self.rect.clip(player_rect)
		killed_player = cropped_rect.width < cropped_rect.height and not is_dashing
		
		if not killed_player:
			self.hp -= 1
			# print("Remaining HP: " + str(self.hp))
			self.elapsed_dmg_cooldown = self.dmg_cooldown

			trigger("Boss Damaged", 0)
			self.action = "DAMAGED"
			self.frame = 0

			if self.hp == 0:
				trigger("Enemy Killed", (self.rect.x, self.rect.y))
				trigger("Boss Killed", 0)
			else:
				return NONE
			
		return KILLED_PLAYER if killed_player else GET_KILLED

	def render(self, display, scroll):
		# debug_rect = pygame.Rect(self.rect.x - scroll[0], self.rect.y - scroll[1], self.rect.width, self.rect.height)
		# pygame.draw.rect(display, (255, 0, 0), debug_rect, 1)

		# if self.atk_target != None:
		# 	debug_rect = pygame.Rect(self.atk_target.x - scroll[0], self.atk_target.y - scroll[1], self.atk_target.width, self.atk_target.height)
		# 	pygame.draw.rect(display, (255, 0, 0), debug_rect, 1)

		self.flip = self.move_dir_mult > 0

		if self.action == 'DAMAGED':
			if self.frame == (len(self.anim_db[self.action]) - 1):
				self.action = 'FLY'

			self.frame += 1
		else:
			self.frame = (self.frame + 1) if self.frame < (len(self.anim_db[self.action]) - 1) else 0

		img_id = self.anim_db[self.action][self.frame]
		sprite = animation_frames[img_id]
		display.blit(pygame.transform.flip(sprite, self.flip, False), (self.rect.x - scroll[0] - self.sprite_offset[0], self.rect.y - scroll[1] - self.sprite_offset[1]))

opossum_anim_db = {}
opossum_anim_db['RUN'] = load_anim(sprites_root + 'opossum', [5, 5, 5, 5, 5, 5])