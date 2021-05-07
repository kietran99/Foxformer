from event_channel import add_listener, trigger

class GameManager:
	def __init__(self):
		self.n_cherries = 0
		self.n_gems = 0
		add_listener("Cherry Obtained", self.on_cherry_obtained)

	def on_cherry_obtained(self, _):
		self.n_cherries += 1
		trigger("Num Cherries Changed", self.n_cherries)