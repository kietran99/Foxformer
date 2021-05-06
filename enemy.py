import pygame

from global_path import *
from animation import *

from map import *





OPOSSUM_WIDTH = 35
OPOSSUM_HEIGHT = 24
OPOSSUM_SPRITE_OFFSET = (0, 2)

PLAYER_DMG_TOP_OFFSET = 26
NOT_COLLIDE = 0
KILLED_PLAYER = 1
GET_KILLED = 2

class Opossum:
	def __init__(self, pos):
		self.move_speed = 2
		# self.move_range = move_range
		# self.pivot_x = pos[0]
		self.move_dir_mult = 1
		self.rect = pygame.Rect(pos[0], pos[1], OPOSSUM_WIDTH, OPOSSUM_HEIGHT)
		# self.sprite = pygame.image.load(sprites_root + 'opossum/opossum_0.png')
		self.flip = False
		self.on_ground = False
		self.action = 'RUN'
		self.frame = 0

	def move(self, tiles):
		self.rect.x += self.move_speed * self.move_dir_mult

		if collision_test(self.rect, tiles):
			self.move_dir_mult *= -1

		if self.on_ground:
			ground_check_rect = self.rect.copy()
			ground_check_rect.x += OPOSSUM_WIDTH
			ground_check_rect.y += OPOSSUM_HEIGHT
			hit_list = collision_test(ground_check_rect, tiles)
			if not hit_list:
				self.move_dir_mult *= -1
			return

		self.rect.y += 16
		hit_list = collision_test(self.rect, tiles)
		self.rect.bottom = hit_list[0].top
		self.on_ground = True

		# if abs(self.rect.x - self.pivot_x) > self.move_range:

	def test_player_collision(self, player_rect):
		if not self.rect.colliderect(player_rect):
			return NOT_COLLIDE

		killed_player = (self.rect.top + PLAYER_DMG_TOP_OFFSET - player_rect.bottom) > (player_rect.right - self.rect.left)
		return KILLED_PLAYER if killed_player else GET_KILLED

	def render(self, display, scroll):
		# debug_rect = pygame.Rect(self.rect.x - scroll[0], self.rect.y - scroll[1], self.rect.width, self.rect.height)
		# pygame.draw.rect(display, (255, 0, 0), debug_rect, 1)
		self.flip = self.move_dir_mult > 0
		self.frame = (self.frame + 1) if self.frame < (len(opossum_anim_db[self.action]) - 1) else 0
		img_id = opossum_anim_db[self.action][self.frame]
		sprite = animation_frames[img_id]
		display.blit(pygame.transform.flip(sprite, self.flip, False), (self.rect.x - scroll[0] - OPOSSUM_SPRITE_OFFSET[0], self.rect.y - scroll[1] - OPOSSUM_SPRITE_OFFSET[1]))

opossum_anim_db = {}
opossum_anim_db['RUN'] = load_anim(sprites_root + 'opossum', [5, 5, 5, 5, 5, 5])