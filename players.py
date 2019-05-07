import numpy as np

class Player:

	def __init__(self):
		self.total_reward = 0
		self.avg_reward = 0
		self.plays = 0

	def action(self, gamestate, player_ind):
		raise NotImplementedError()

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

class AlternateCooperateFlipPlayer(Player):
	def action(self, gamestate, player_ind):
		if len(gamestate) % 2 == 0:
			return 0
		else:
			return (np.random.rand(1) > 0.5)[0]

class LastCheatPlayerPlayer(Player):
	def action(self, gamestate, player_ind):
		if len(gamestate) < 98:
			return 0
		else:
			return 1

class RandomPlayer(Player):
	def action(self, gamestate, player_ind):
		return (np.random.rand(1) > 0.5)[0]

class AlternatePlayer(Player):
	def action(self, gamestate, player_ind):
		if len(gamestate) % 2 == 0:
			return 0
		else:
			return 1
