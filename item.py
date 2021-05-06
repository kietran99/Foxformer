import pygame

from global_path import *

from animation import *





CHERRY_SIZE = (19, 16)
CHERRY_Y = 4
CHERRY_SPRITE_OFFSET = (6, 2)

def items_update(items, player_rect, display, scroll):
	obtains = []

	for item in items:
		if item.test_player_collision(player_rect):
			obtains.append(item)
			continue

		item.render(display, scroll)

	return obtains

class Cherry:
	def __init__(self, pos):
		self.rect = pygame.Rect(pos[0], pos[1], CHERRY_SIZE[0], CHERRY_SIZE[1])
		self.action = 'IDLE'
		self.frame = 0

	def test_player_collision(self, player_rect):
		return self.rect.colliderect(player_rect)

	def render(self, display, scroll):
		# debug_rect = pygame.Rect(self.rect.x - scroll[0], self.rect.y - scroll[1], self.rect.width, self.rect.height)
		# pygame.draw.rect(display, (255, 0, 0), debug_rect, 1)
		self.frame = (self.frame + 1) if self.frame < (len(cherry_anim_db[self.action]) - 1) else 0
		img_id = cherry_anim_db[self.action][self.frame]
		sprite = animation_frames[img_id]
		display.blit(sprite, (self.rect.x - scroll[0] - CHERRY_SPRITE_OFFSET[0], self.rect.y - scroll[1] - CHERRY_SPRITE_OFFSET[1]))

items_dict = {
	'7': lambda pos: Cherry((pos[0], pos[1] - CHERRY_Y))
}

cherry_anim_db = {}
cherry_anim_db['IDLE'] = load_anim(sprites_root + 'cherry', [7, 7, 7, 7, 7, 7, 7])