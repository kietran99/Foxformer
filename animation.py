import pygame

from global_path import *





def load_anim(path, frame_duration):
	global animation_frames
	animation_name = path.split('/')[-1]
	animation_frame_data = []
	n = 0
	for frame in frame_duration:
		animation_frame_id = animation_name + '_' + str(n)
		img_loc = path + '/' + animation_frame_id + '.png'
		animation_img = pygame.image.load(img_loc)
		animation_frames[animation_frame_id] = animation_img.copy()
		animation_frame_data.extend([animation_frame_id for _ in range(frame)])
		n += 1

	return animation_frame_data

def change_action(action_var, frame, new_val):
	if action_var != new_val:
		action_var = new_val
		frame = 0

	return action_var, frame

sprites_root = image_root + 'sprites/'

animation_frames = {}

