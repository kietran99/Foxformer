from utils import foreach

class Event:
	def __init__(self):
		self.__listeners = []

	def add_listener(self, listener):
		self.__listeners.append(listener)

	def remove_listener(self, listener):
		self.__listeners.remove(listener)

	def trigger(self, event_data):
		foreach(lambda listener: listener(event_data), self.__listeners)

event_dict = {}

def add_listener(name, listener):
	if name not in event_dict:
		event_dict[name] = Event()
	
	event_dict[name].add_listener(listener)

def remove_listener(name, listener):
	if name in event_dict:
		event_dict[name].remove_listener(listener)

def trigger(name, event_data):
	if name not in event_dict:
		event_dict[name] = Event()

	event_dict[name].trigger(event_data)