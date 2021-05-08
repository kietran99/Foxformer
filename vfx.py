import pygame

from global_path import *
from event_channel import add_listener

from animation import *

class VFX:
	def __init__(self):
		self.action = 'PLAY'
		self.frame = 0
		self.anim_db = {}

	def next_frame_id(self):
		if self.frame < (len(self.anim_db[self.action])):
			self.frame += 1	
			return self.anim_db[self.action][self.frame - 1], False

		self.frame = 0
		return None, True

class EnemyDeath(VFX):
	def __init__(self):
		super().__init__()
		self.anim_db['PLAY'] = load_anim(sprites_root + 'enemy-death', [7, 7, 7, 7, 7, 7])

class RareItemObtain(VFX):
	def __init__(self):
		super().__init__()
		self.anim_db['PLAY'] = load_anim(sprites_root + 'rare-item-obtain', [7, 7, 7, 7])

class VFXManager:
	def __init__(self):
		self.active = False
		self.pos = (0, 0)
		self.sprite_offset = (0, 8)

		self.all_vfx = {
			'ENEMY DEATH': EnemyDeath(),
			'RARE ITEM OBTAIN': RareItemObtain()
		}

		self.cur_vfx = None
		add_listener("Enemy Killed", self.on_enemy_killed)
		add_listener("Rare Item Obtained", self.on_rare_item_obtained)

	def on_enemy_killed(self, data):
		self.active = True
		self.pos = data
		self.cur_vfx = self.all_vfx['ENEMY DEATH']

	def on_rare_item_obtained(self, data):
		self.active = True
		self.pos = data
		self.cur_vfx = self.all_vfx['RARE ITEM OBTAIN']

	def render(self, display, scroll):
		if not self.active:
			return

		next_frame_id, finished = self.cur_vfx.next_frame_id()

		if finished:
			self.active = False
			return

		sprite = animation_frames[next_frame_id]
		display.blit(sprite, (self.pos[0] - scroll[0] - self.sprite_offset[0], self.pos[1] - scroll[1] - self.sprite_offset[1]))