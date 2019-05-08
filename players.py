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
		if gamestate["current_iter"] > 1:
			return gamestate["moves"][-1][1-player_ind]
		else:
			return 0

class AlternateCooperateFlipPlayer(Player):
	def action(self, gamestate, player_ind):
		return 1
		if gamestate["current_iter"] % 2 == 1:
			return 0
		else:
			return (np.random.rand(1) > 0.5)[0]

class LastCheatPlayer(Player):
	def action(self, gamestate, player_ind):
		if gamestate["current_iter"] < gamestate["n_iter"]:
			return 0
		else:
			return 1

class RandomPlayer(Player):
	def action(self, gamestate, player_ind):
		return (np.random.rand(1) > 0.5)[0]

class AlternatePlayer(Player):
	def action(self, gamestate, player_ind):
		if gamestate["current_iter"] % 2 == 1:
			return 0
		else:
			return 1

class GrudgerPlayer(Player):
	def __init__(self):
		super(GrudgerPlayer, self).__init__()
		self.cheated = False
	def action(self, gamestate, player_ind):
		if gamestate["current_iter"] > 1:
			if gamestate["moves"][-1][1-player_ind] == 1:
				self.cheated = True
			if not self.cheated:
				return 0
			else:
				return 1
		else:
			self.cheated = False
			return 0

class BayesianPlayer(Player):
	def __init__(self, otherplayers):
		super(BayesianPlayer, self).__init__()
		self.player_types = otherplayers
		self.reset()

	def action(self, gamestate, player_ind):
		return 0
		if not gamestate:
			self.reset()
		else:
			self.update(gamestate, player_ind)
		opponent_type = max(self.beliefs.keys(), key = lambda k: self.beliefs[k])
		act = self.best_respose(opponent_type)
		return act

	def update(self, gamestate, player_ind):

		moves = np.asarray(gamestate["moves"])[:, [player_ind, 1-player_ind]]

		prev_self_move, prev_opponent_move = moves[-1, 0], moves[-1, 1]
		prev_prev_self_move, prev_prev_opponent_move = moves[-2, 0], moves[-2, 1]

		for opponent_type in self.beliefs:

			if opponent_type == NicePlayer:
				p_data_given_type = 1 if prev_opponent_move == 0 else 0
			elif opponent_type == MeanPlayer:
				p_data_given_type = 1 if prev_opponent_move == 1 else 0
			elif opponent_type == TitForTatPlayer:
				p_data_given_type = 1 if prev_opponent_move == prev_prev_self_move else 0
			elif opponent_type == AlternateCooperateFlipPlayer:
				if gamestate["current_iter"] % 2 == 1:
					return 0
				else:
					return (np.random.rand(1) > 0.5)[0]
			elif opponent_type == LastCheatPlayer:
				if gamestate["current_iter"] < gamestate["n_iter"]:
					return 0
				else:
					return 1
			elif opponent_type == RandomPlayer:
				pass
			elif opponent_type == AlternatePlayer:
				if gamestate["current_iter"] % 2 == 1:
					return 0
				else:
					return 1
			elif opponent_type == BayesianPlayer:
				continue
			else:
				raise ValueError("Invalid player type.")

			p_type = self.beliefs[opponent_type]
			p_data = 0.5
			p_type_given_data = p_data_given_type * p_type / p_data
			self.beliefs[opponent_type] = p_type_given_data

	def reset(self):
		self.beliefs = {p_type: 1/len(self.player_types) for p_type in self.player_types}

	def best_respose(self, opponent_type, gamestate, player_ind):

		moves = np.asarray(gamestate["moves"])[:, [player_ind, 1-player_ind]]
		prev_self_move, prev_opponent_move = moves[-1, 0], moves[-1, 1]

		if opponent_type == NicePlayer:
			return MeanPlayer.action(gamestate, player_ind)
		elif opponent_type == MeanPlayer:
			return MeanPlayer.action(gamestate, player_ind)
		elif opponent_type == TitForTatPlayer:
			pass
		elif opponent_type == AlternateCooperateFlipPlayer:
			pass
		elif opponent_type == LastCheatPlayer:
			return MeanPlayer().action(gamestate, player_ind)
		elif opponent_type == RandomPlayer:
			return MeanPlayer().action(gamestate, player_ind)
		elif opponent_type == AlternatePlayer:
			pass
		elif opponent_type == BayesianPlayer:
			return MeanPlayer().action(gamestate, player_ind)
		else:
			raise ValueError("Invalid player type.")
