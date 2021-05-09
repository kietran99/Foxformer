import pygame

from global_path import *
from animation import *
from event_channel import trigger

from map import *




OPOSSUM_WIDTH = 35
OPOSSUM_HEIGHT = 24
OPOSSUM_SPRITE_OFFSET = (0, 2)
OPOSSUM_Y = 7

PLAYER_DMG_TOP_OFFSET = 27

NOT_COLLIDE = 0
KILLED_PLAYER = 1
GET_KILLED = 2



def enemies_update(enemies, tile_rects, player_rect, display, scroll):
	killed_player = False
	dead_enemies = []

	for enemy in enemies:
		enemy.move(tile_rects)
		collision_res = enemy.test_player_collision(player_rect)
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

	def move(self, tiles):
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

	def test_player_collision(self, player_rect):
		if not self.rect.colliderect(player_rect):
			return NOT_COLLIDE

		cropped_rect = self.rect.clip(player_rect)
		# print("W: " + str(cropped_rect.width) + " H: " + str(cropped_rect.height))
		killed_player = cropped_rect.width < cropped_rect.height

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

opossum_anim_db = {}
opossum_anim_db['RUN'] = load_anim(sprites_root + 'opossum', [5, 5, 5, 5, 5, 5])