import pygame

from global_path import *
from event_channel import trigger

from animation import *





def items_update(items, player_rect, display, scroll):
	obtains = []

	for item in items:
		collide, obtainable = item.test_player_collision(player_rect)

		if collide and obtainable:
			obtains.append(item)
			continue

		item.render(display, scroll)

	return obtains

class Item:
	def __init__(self, pos, size, sprite_offset):
		self.rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
		self.sprite_offset = sprite_offset
		self.obtainable = True
		self.action = 'IDLE'
		self.frame = 0
		self.anim_db = {}

	def test_player_collision(self, player_rect):
		res = self.rect.colliderect(player_rect)

		if res:
			self.on_player_collide(player_rect)

		return res, self.obtainable

	def on_player_collide(self, player_rect):
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

	def on_player_collide(self, player_rect):
		trigger("Cherry Obtained", 0)

class Gem(Item):
	def __init__(self, pos, size, sprite_offset):
		super().__init__(pos, size, sprite_offset)
		self.anim_db['IDLE'] = load_anim(sprites_root + 'gem', [7, 7, 7, 7, 7])

	def on_player_collide(self, player_rect):
		trigger("Gem Obtained", 0)
		trigger("Rare Item Obtained", (self.rect.x, self.rect.y))






class Prop(Item):
	def __init__(self, pos, size, sprite_offset):
		super().__init__(pos, size, sprite_offset)
		self.obtainable = False

class Spring(Prop):
	def __init__(self, pos, size, sprite_offset):
		super().__init__(pos, size, sprite_offset)
		self.anim_db['IDLE'] = load_anim(sprites_root + 'spring', [1])

	def on_player_collide(self, player_rect):
		trigger("On Spring Collide", 0)





class Quirk(Prop):
	def __init__(self, pos, size, sprite_offset):
		super().__init__(pos, size, sprite_offset)
		self.action = 'CRATE'
		self.anim_db['CRATE'] = load_anim(sprites_root + 'crate', [1])

	def test_player_collision(self, player_rect):
		if not self.rect.colliderect(player_rect):
			return False, self.obtainable

		if self.action == 'OBTAIN':
			self.on_player_collide(player_rect)
			return True, self.obtainable

		cropped_rect = self.rect.clip(player_rect)
		broken = cropped_rect.width >= cropped_rect.height and cropped_rect.width >= self.rect.width * 0.3

		if broken:
			self.action, self.frame = change_action(self.action, self.frame, 'OBTAIN')
			self.obtainable = True
			trigger("On Crate Broken", 0)
		else:
			if player_rect.left < self.rect.left:
				player_rect.right = self.rect.left
			else:
				player_rect.left = self.rect.right
			
		return True, False

class Weed(Quirk):
	def __init__(self, pos, size, sprite_offset):
		super().__init__(pos, size, sprite_offset)
		self.anim_db['OBTAIN'] = load_anim(sprites_root + 'weed', [7, 7, 7, 7, 7])

	def on_player_collide(self, player_rect):
		trigger("On Weed Obtained", 0)
		trigger("Rare Item Obtained", (self.rect.x, self.rect.y))