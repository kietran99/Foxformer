import pygame

from global_path import *
from event_channel import trigger

from animation import *





CHERRY_SIZE = (19, 16)
CHERRY_Y = 4
CHERRY_SPRITE_OFFSET = (6, 2)

GEM_Y = 2

def items_update(items, player_rect, display, scroll):
	obtains = []

	for item in items:
		if item.test_player_collision(player_rect):
			obtains.append(item)
			continue

		item.render(display, scroll)

	return obtains

class Item:
	def __init__(self, pos, size, sprite_offset):
		self.rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
		self.sprite_offset = sprite_offset
		self.action = 'IDLE'
		self.frame = 0
		self.anim_db = {}

	def test_player_collision(self, player_rect):
		res = self.rect.colliderect(player_rect)

		if res:
			self.on_player_collide()

		return res

	def on_player_collide(self):
		pass

	def render(self, display, scroll):
		# debug_rect = pygame.Rect(self.rect.x - scroll[0], self.rect.y - scroll[1], self.rect.width, self.rect.height)
		# pygame.draw.rect(display, (255, 0, 0), debug_rect, 1)
		self.frame = (self.frame + 1) if self.frame < (len(self.anim_db[self.action]) - 1) else 0
		img_id = self.anim_db[self.action][self.frame]
		sprite = animation_frames[img_id]
		display.blit(sprite, (self.rect.x - scroll[0] - self.sprite_offset[0], self.rect.y - scroll[1] - self.sprite_offset[1]))

class Cherry(Item):
	def __init__(self, pos, size, sprite_offset):
		super().__init__(pos, size, sprite_offset)
		self.anim_db['IDLE'] = load_anim(sprites_root + 'cherry', [7, 7, 7, 7, 7, 7, 7])

	def on_player_collide(self):
		trigger("Cherry Obtained", 0)

class Gem(Item):
	def __init__(self, pos, size, sprite_offset):
		super().__init__(pos, size, sprite_offset)
		self.anim_db['IDLE'] = load_anim(sprites_root + 'gem', [7, 7, 7, 7, 7])

	def on_player_collide(self):
		trigger("Gem Obtained", 0)


