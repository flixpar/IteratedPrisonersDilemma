class Player:

	def __init__(self):
		self.total_reward = 0
		self.avg_reward = 0
		self.plays = 0

	def action(self, gamestate, player_ind):
		raise NotImplementedError()

	def update_beliefs(self):
		pass

	def reward(self, r):
		self.total_reward += r
		self.plays += 1
		self.avg_reward = self.total_reward / self.plays

class NicePlayer(Player):
	def action(self, gamestate, player_ind):
		return 0

class MeanPlayer(Player):
	def action(self, gamestate, player_ind):
		return 1

class TitForTatPlayer(Player):
	def action(self, gamestate, player_ind):
		if gamestate:
			return gamestate[-1][1-player_ind]
		else:
			return 0
