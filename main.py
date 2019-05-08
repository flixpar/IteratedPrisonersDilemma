import random

from game import GameState
import players

player_types = [
	players.NicePlayer,
	players.MeanPlayer,
	players.TitForTatPlayer,
	players.GrudgerPlayer,
	players.RandomPlayer,
	players.LastCheatPlayer,
	players.AlternateCooperateFlipPlayer,
	# players.AlternatePlayer,
	# players.BayesianPlayer,
]

def main():

	# generate players
	players = generate_mixed_player_pool(10)

	# play games between random players
	for _ in range(2):
		for i in range(len(players)):
			for j in range(i+1, len(players)):
				p1, p2 = players[i], players[j]
				game = GameState(p1, p2, iterations=100)
				r1, r2 = game.play()
				p1.reward(r1)
				p2.reward(r2)

	#  display rewards
	rewards = rewards_by_playertype(players)
	for p_type, outcome in rewards.items():
		print(f"Average score for {p_type.__name__}: {outcome[0]/outcome[1]:.3f}")

def generate_random_player_pool(n=100):
	players = []
	for _ in range(n):
		players.append(random_player())
	return players

def generate_mixed_player_pool(n=10):
	players = []
	for p_type in player_types:
		for _ in range(n):
			players.append(p_type())
	random.shuffle(players)
	return players

def rewards_by_playertype(players):
	rewards = {p_type: [0, 0] for p_type in player_types}
	for player in players:
		p_type = type(player)
		rewards[p_type][0] += player.avg_reward
		rewards[p_type][1] += 1
	return rewards

def random_player():
	player = random.choice(player_types)
	return player()

if __name__ == "__main__":
	main()
