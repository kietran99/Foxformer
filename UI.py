import pygame
from pygame.locals import *

from global_path import *
from config import *
from event_channel import add_listener, trigger

from map import render_bg

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
		self.n_cherries_text = Text('0', 48, (255, 255, 255), (140, 60), True)

		self.gem_active_states = [False, False, False]
		self.gem_inactive_icon = pygame.image.load(sprites_root + 'UI/gem-inactive-icon.png')
		self.gem_active_icon = pygame.image.load(sprites_root + 'UI/gem-active-icon.png')
		self.gem_icon_pos_list = [(7, 26), (23, 26), (39, 26)]

		self.is_weed_active = False
		self.weed_inactive_icon = pygame.image.load(sprites_root + 'UI/weed-inactive-icon.png')
		self.weed_active_icon = pygame.image.load(sprites_root + 'UI/weed-active-icon.png')
		self.weed_icon_pos = (280, 6)

		self.is_pipe_active = False
		self.pipe_inactive_icon = pygame.image.load(sprites_root + 'UI/pipe-inactive-icon.png')
		self.pipe_active_icon = pygame.image.load(sprites_root + 'UI/pipe-active-icon.png')
		self.pipe_icon_pos = (260, 6)

		add_listener("Num Cherries Changed", self.on_n_cherries_changed)
		add_listener("Num Gems Changed", self.on_n_gems_changed)
		add_listener("On Weed Obtained", self.on_weed_obtained)
		add_listener("On Pipe Obtained", self.on_pipe_obtained)

	def on_n_cherries_changed(self, n_cherries):
		self.n_cherries_text.text = str(n_cherries)

	def on_n_gems_changed(self, _):
		for i in range(len(self.gem_active_states)):
			if not self.gem_active_states[i]:
				self.gem_active_states[i] = True
				break

	def on_weed_obtained(self, _):
		self.is_weed_active = True

	def on_pipe_obtained(self, _):
		self.is_pipe_active = True

	def render(self, window):
		display = pygame.Surface((WINDOW_SIZE[0] / RESOLUTION, WINDOW_SIZE[1] / RESOLUTION), SRCALPHA)

		display.blit(self.cherry_icon, self.cherry_icon_pos)
		
		for i in range(len(self.gem_active_states)):
			display.blit(self.gem_active_icon if self.gem_active_states[i] else self.gem_inactive_icon, self.gem_icon_pos_list[i])

		display.blit(self.weed_active_icon if self.is_weed_active else self.weed_inactive_icon, self.weed_icon_pos)
		display.blit(self.pipe_active_icon if self.is_pipe_active else self.pipe_inactive_icon, self.pipe_icon_pos)

		surface = pygame.transform.scale(display, WINDOW_SIZE)
		window.blit(surface, (0, 0))

		canvas = pygame.Surface(WINDOW_SIZE, SRCALPHA)
		self.n_cherries_text.render(canvas)
		window.blit(canvas, (0, 0))

class MainMenu:
	def __init__(self, display):
		self.display = display
		self.text_size = 48
		self.text_color = (195, 165, 39)

		self.container = pygame.image.load(sprites_root + "UI/panel.png")
		self.new_game_text = Text("New Game (N)", self.text_size, self.text_color, (600, 300), False)
		self.option_text =   Text("Option   (O)", self.text_size, self.text_color, (600, 400), False)
		self.about_text =    Text("About    (A)", self.text_size, self.text_color, (600, 500), False)
		self.exit_text =     Text("Exit     (X)", self.text_size, self.text_color, (600, 600), False)
		
		self.is_about = False
		self.about_content_text_0 = Text('Art by Ansimuz and Kietran99', self.text_size, self.text_color, (600, 400), True)
		self.about_content_text_1 = Text('Music by Pascal Belisle', self.text_size, self.text_color, (600, 500), True)
		self.return_text = Text("Return     (R)", self.text_size, self.text_color, (600, 700), False)

		self.is_option = False
		self.option_content_text = Text("NOTHING HAHAHA", self.text_size + 16, self.text_color, (600, 400), True)

	def handle_input(self, event):
		if event.type != KEYDOWN:
			return

		if event.key == K_n:
			trigger("New Game", 0)

		elif event.key == K_x:
			trigger("Exit Game", 0)

		elif event.key == K_r:
			if self.is_about:
				self.is_about = False
			elif self.is_option:
				self.is_option = False

		elif not self.is_about and event.key == K_a:
			self.is_about = True

		elif not self.is_option and event.key == K_o:
			self.is_option = True

	def render(self, window):
		render_bg(self.display, (0, 0))

		if not self.is_about and not self.is_option:
			self.display.blit(self.container, (70, 50))
	
		surface = pygame.transform.scale(self.display, WINDOW_SIZE)
		window.blit(surface, (0, 0))

		canvas = pygame.Surface(WINDOW_SIZE, SRCALPHA)

		if self.is_about:
			self.about_content_text_0.render(canvas)
			self.about_content_text_1.render(canvas)
			self.return_text.render(canvas)
		elif self.is_option:
			self.option_content_text.render(canvas)
			self.return_text.render(canvas)
		else:
			self.new_game_text.render(canvas)
			self.option_text.render(canvas)
			self.about_text.render(canvas)
			self.exit_text.render(canvas)
		
		window.blit(canvas, (0, 0))

class EndGameMenu:
	def __init__(self):
		self.container = pygame.image.load(sprites_root + "UI/panel.png")
		self.container_pos = (70, 40)

		self.won_lose_text_size = 64
		self.won_text = Text('CONGRATS', self.won_lose_text_size, (53, 235, 127), (WINDOW_SIZE[0] / 2, WINDOW_SIZE[1] / 2 - 180), True)
		self.lose_text = Text('HAHAHA!!', self.won_lose_text_size, (189, 25, 25), (WINDOW_SIZE[0] / 2, WINDOW_SIZE[1] / 2 - 180), True)

		self.cherry_icon = pygame.image.load(sprites_root + 'cherry/cherry_3.png')
		self.cherry_icon_pos = (120, 70)
		self.n_cherries_text = Text('0', 64, (255, 255, 255), (WINDOW_SIZE[0] / 2 + 10, WINDOW_SIZE[1] / 2 - 85), True)

		self.gem_inactive_icon = pygame.image.load(sprites_root + 'UI/gem-inactive-icon.png')
		self.gem_active_icon = pygame.image.load(sprites_root + 'UI/gem-active-icon.png')
		gem_icon_y = 100
		gem_icon_start_x = 118
		self.gem_icon_pos_list = [(gem_icon_start_x, gem_icon_y), (gem_icon_start_x + 24, gem_icon_y), (gem_icon_start_x + 48, gem_icon_y)]

		self.text_size = 32
		self.play_again_text = Text("Play Again (P)", self.text_size, (230, 233, 56), (600, 560), True)
		self.exit_text =     Text("Exit (X)", self.text_size, (189, 25, 25), (600, 610), True)

	def handle_input(self, event):
		if event.type != KEYDOWN:
			return

		if event.key == K_p:
			trigger("Play Again", 0)

		elif event.key == K_x:
			trigger("Exit Game", 0)

	def render(self, display, window, has_won, n_cherries, n_gems):
		display.blit(self.container, self.container_pos)

		display.blit(self.cherry_icon, self.cherry_icon_pos)
	
		gem_active_states = [i < n_gems for i in range(3)]
		for i in range(len(gem_active_states)):
			display.blit(self.gem_active_icon if gem_active_states[i] else self.gem_inactive_icon, self.gem_icon_pos_list[i])

		surface = pygame.transform.scale(display, WINDOW_SIZE)
		window.blit(surface, (0, 0))

		canvas = pygame.Surface(WINDOW_SIZE, SRCALPHA)

		if has_won:
			self.won_text.render(canvas)
		else:
			self.lose_text.render(canvas)

		self.n_cherries_text.text = str(n_cherries)
		self.n_cherries_text.render(canvas)
		self.play_again_text.render(canvas)
		self.exit_text.render(canvas)
		
		window.blit(canvas, (0, 0))