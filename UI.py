import pygame
from pygame.locals import *

from global_path import *
from config import *
from event_channel import add_listener

FONT_PATH = 'fonts/VCR_OSD_MONO_1.001.ttf'

class Text:
	def __init__(self, text: str, size: int, color: tuple[int, int, int], pos: tuple[int, int], bold):
		self.text = text
		self.__size = size
		self.__color = color
		self.__pos = pos
		self.__font = pygame.font.Font(FONT_PATH, self.__size)
		self.__font.set_bold(bold)

	def render(self, window):
		render_text_fn = self.__bind(window, self.__font)
		render_text_fn(self.text, self.__color, self.__pos)

	def outlined_render(self, window):
		render_fn = self.__outlined_bind(window, self.__font)
		render_fn(self.text, self.__color, self.__pos)

	def __bind(self, window, font):
		return lambda text, color, pos: self.__render_number(window, font, int(text), color, pos) if text.isdigit() else \
    		self.__render_text(window, font, text, color, pos)

	def __outlined_bind(self, window, font):
		return lambda text, color, pos: self.__outlined_render_number(window, font, int(text), color, pos) if text.isdigit() else \
		self.__outlined_render_text(window, font, text, color, pos)

	def __render_number(self, window, font, text : int, color: tuple[int, int, int], pos: tuple[int, int]):
		self.__render_text(window, font, self._format_num(text), color, pos)

	def _format_num(self, num: int):
		return ("0" if num < 10 else "") + str(num)

	def __render_text(self, window, font, text : str, color: tuple[int, int, int], pos: tuple[int, int]):
		time_text = font.render(text, True, color)
		time_text_rect = time_text.get_rect()
		time_text_rect.center = pos
		window.blit(time_text, time_text_rect)

	def __outlined_render_number(self, window, font, text : int, color: tuple[int, int, int], pos: tuple[int, int]):
		self.__outlined_render_text(window, font, self._format_num(text), color, pos)

	def __outlined_render_text(self, window, font, text : str, color: tuple[int, int, int], pos: tuple[int, int]):
		text = font.render(text, True, color)
		text_rect = text.get_rect()
		text_rect.center = pos
		window.blit(text, text_rect)

		mask = pygame.mask.from_surface(window)
		mask_outline = mask.outline()
		n = 0
		for point in mask_outline:
			mask_outline[n] = (point[0] + text_rect.x - 90, point[1] + text_rect.y)
			n += 1
		# print(mask_outline)
		pygame.draw.polygon(window, (0, 0, 0), mask_outline, 3)

class UICanvas:
	def __init__(self):
		self.cherry_icon = pygame.image.load(sprites_root + 'cherry/cherry_3.png')
		self.cherry_icon_pos = (3, 3)
		self.n_cherries_text = Text('0', 48, (255, 255, 255), (140, 70), True)

		self.gem_icon = pygame.image.load(sprites_root + 'gem/gem_1.png')
		self.gem_icon_pos = (7, 26)
		self.n_gems_text = Text('0', 48, (255, 255, 255), (140, 130), True)

		self.should_show_weed = False
		self.weed_icon = pygame.image.load(sprites_root + 'weed/weed_0.png')
		self.weed_icon_pos = (280, 6)

		add_listener("Num Cherries Changed", self.on_n_cherries_changed)
		add_listener("Num Gems Changed", self.on_n_gems_changed)
		add_listener("On Weed Obtained", self.on_weed_obtained)

	def on_n_cherries_changed(self, n_cherries):
		self.n_cherries_text.text = str(n_cherries)

	def on_n_gems_changed(self, n_gems):
		self.n_gems_text.text = str(n_gems)

	def on_weed_obtained(self, _):
		self.should_show_weed = True

	def render(self, window):
		display = pygame.Surface((WINDOW_SIZE[0] / RESOLUTION, WINDOW_SIZE[1] / RESOLUTION), SRCALPHA)

		display.blit(self.cherry_icon, self.cherry_icon_pos)
		display.blit(self.gem_icon, self.gem_icon_pos)
		if self.should_show_weed:
			display.blit(self.weed_icon, self.weed_icon_pos)

		surface = pygame.transform.scale(display, WINDOW_SIZE)
		window.blit(surface, (0, 0))

		canvas = pygame.Surface(WINDOW_SIZE, SRCALPHA)
		self.n_cherries_text.render(canvas)
		self.n_gems_text.render(canvas)
		window.blit(canvas, (0, 0))