class GameState:

	def __init__(self, player1, player2, iterations=100):
		self.player1 = player1
		self.player2 = player2
		self.n_iter = iterations
		self.state = []

	def play(self):
		rewards = [0, 0]
		for _ in range(self.n_iter):
			p1, p2 = self.player1.action(self.state, 0), self.player2.action(self.state, 1)
			self.state.append((p1, p2))
			if p1 == 0 and p2 == 0:
				rewards[0] += 2
				rewards[1] += 2
			elif p1 == 0 and p2 == 1:
				rewards[0] += -1
				rewards[1] += 3
			elif p1 == 1 and p2 == 0:
				rewards[0] += 3
				rewards[1] += -1
			elif p1 == 1 and p2 == 1:
				rewards[0] += 0
				rewards[1] += 0
		return rewards[0] / self.n_iter, rewards[1] / self.n_iter
