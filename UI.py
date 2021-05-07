import pygame
from pygame.locals import *

from global_path import *
from config import *
from event_channel import add_listener

FONT_PATH = 'fonts/VCR_OSD_MONO_1.001.ttf'

class Text:
	def __init__(self, text: str, size: int, color: tuple[int, int, int], pos: tuple[int, int]):
		self.text = text
		self.__size = size
		self.__color = color
		self.__pos = pos

	def render(self, window):
		render_text_fn = self.__bind(window, pygame.font.Font(FONT_PATH, self.__size))
		render_text_fn(self.text, self.__color, self.__pos)

	def __bind(self, window, font):
		return lambda text, color, pos: self.__render_number(window, font, int(text), color, pos) if text.isdigit() else \
    		self.__render_text(window, font, text, color, pos)

	def __render_number(self, window, font, text : int, color: tuple[int, int, int], pos: tuple[int, int]):
		self.__render_text(window, font, self._format_num(text), color, pos)

	def _format_num(self, num: int):
		return ("0" if num < 10 else "") + str(num)

	def __render_text(self, window, font, text : str, color: tuple[int, int, int], pos: tuple[int, int]):
		time_text = font.render(text, True, color)
		time_text_rect = time_text.get_rect()
		time_text_rect.center = pos
		window.blit(time_text, time_text_rect)

class UICanvas:
	def __init__(self):
		self.cherry_icon = pygame.image.load(sprites_root + 'cherry/cherry_3.png')
		self.cherry_icon_pos = (3, 3)
		self.n_cherries_text = Text('0', 48, (255, 255, 255), (140, 70))

		self.gem_icon = pygame.image.load(sprites_root + 'gem/gem_1.png')
		self.gem_icon_pos = (7, 26)
		self.n_gems_text = Text('0', 48, (255, 255, 255), (140, 130))

		add_listener("Num Cherries Changed", self.on_n_cherries_changed)
		add_listener("Num Gems Changed", self.on_n_gems_changed)

	def on_n_cherries_changed(self, n_cherries):
		self.n_cherries_text.text = str(n_cherries)

	def on_n_gems_changed(self, n_gems):
		self.n_gems_text.text = str(n_gems)

	def render(self, window):
		display = pygame.Surface((WINDOW_SIZE[0] / RESOLUTION, WINDOW_SIZE[1] / RESOLUTION), SRCALPHA)

		display.blit(self.cherry_icon, self.cherry_icon_pos)
		display.blit(self.gem_icon, self.gem_icon_pos)

		surface = pygame.transform.scale(display, WINDOW_SIZE)
		window.blit(surface, (0, 0))

		self.n_cherries_text.render(window)
		self.n_gems_text.render(window)