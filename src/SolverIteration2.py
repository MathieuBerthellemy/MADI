import numpy as np
import math

class SolverIteration2:
	def __init__(self, grid, weight):
		self.grid = grid
		self.weight = weight

		self.gamma = self.compute_gamma()
		self.epsilon = 0.5
		
		self.Vs = []
		self.Q_at = []
		self.t = -1

		# iteration dans le vide pour init
		self.nouvelle_iteration()

		# lancement de l'algo
		self.iteration_de_la_valeur()
		self.values = self.Vs[self.t-1]
		self.solution = self.convert()
		# print self.values
		# print self.solution

	def compute_gamma(self):
		width = self.grid.shape[0]
		height = self.grid.shape[1]

		D = width+height
		output = 0.5
		output_bounds = (0, 1)

		window = (5, 10)
		while True:

			tmp = self.get_reward(width-1, height-1)
			for i in range(int(D/4)):
				tmp = math.pow(tmp, output)
		
			# Si en dessous de la fenetre
			if tmp < window[0]:
				output_bounds = (output, output_bounds[1])

			# S au dessus de la fenetre
			elif tmp > window[1]:
				output_bounds = (output_bounds[0], output)
			# Si dans la fenetre
			else:
				break

			output = (output_bounds[0] + output_bounds[1])/2
			#print output, ": ", output_bounds, ", ", tmp

		#print "gamma = ", output
		return output

	def get_move(self, x , y):
		return self.solution[x, y]

	def convert(self):
		output = np.chararray(self.grid.shape)
		
		for (lin, col) in self.get_S():
			best_v = 0
			for action, (lin_n, col_n) in self._get_neighborhood(lin, col):
				if self.Vs[self.t-1][lin_n][col_n] > best_v:
					output[lin][col] = action
					best_v = self.values[lin_n][col_n]
		return output

	def nouvelle_iteration(self):
		self.t += 1
		self.Vs.append(np.zeros(self.grid.shape))
		self.Q_at.append([[{} for lin in range(self.grid.shape[0])] for col in range(self.grid.shape[1])] )

	def iteration_de_la_valeur(self):
		
		while True:
			self.nouvelle_iteration()
			

			# matrice binaire, 1 -> la case lin/col a deja ete calculee, 0 sinon
			# Pour l'amelioration de Gauss Seidel	
			already_computed = np.zeros(self.grid.shape)

			# pour chaque etat de la grille
			for (lin, col) in self.get_S():
				# Recuperation du voisinage
				neighboorhood = self._get_neighborhood(lin, col)
				# pour chaque action possible
				for action, (lin_n, col_n) in neighboorhood:
					# On calcul Q_at(s)
					esperance = self.get_esperance_utilite(lin_n, col_n, already_computed)
					self.Q_at[self.t][col][lin][action] = self.get_reward(lin, col) + self.gamma * esperance				
				# Vt(s) = malin_a(Q_at(a))
				self.Vs[self.t][lin, col] = max([0]+[value for key, value in self.Q_at[self.t][col][lin].items()])
				already_computed[lin, col] = 1

			if self.get_max_diff_V() <= self.epsilon or self.t > 100:
				break

	def get_max_diff_V(self):
		"""
			retourne la plus grande difference Vt, Vt-1
		"""

		return max([self.Vs[self.t][lin, col] - self.Vs[self.t-1][lin, col] for (lin, col) in self.get_S()])


	def get_esperance_utilite(self, lin, col, already_computed):
		"""
			Retourne l'esperance d'utilite pour l'etat de coordonnees lin, col
		"""
		adjacents = self.get_adjacents(lin, col)
		output = 0
		#amelioration de Gauss Seidel
		if already_computed[lin, col] == 0:
			output += (1-len(adjacents)/16)*self.Vs[self.t-1][lin, col]
		else:
			output += (1-len(adjacents)/16)*self.Vs[self.t][lin, col]
			
		for (lin_a, col_a) in adjacents:
			if already_computed[lin, col] == 0:
				output += self.Vs[self.t-1][lin_a, col_a]/16
			else:
				output += self.Vs[self.t][lin_a, col_a]/16
	
		return output

	def get_adjacents(self, lin, col):
		"""
			Retourne une liste de coordonnees, ceulin des etats adjacents de l'etat de coordonnees lin col
		"""
		output = [(lin+lin_a, col+col_a) for lin_a in [-1, 0, 1] for col_a in [-1, 0, 1] if (lin+lin_a >= 0 and col+col_a >= 0 and lin+lin_a < self.grid.shape[0] and col+col_a < self.grid.shape[1]) and not(lin_a == 0 and col_a == 0)]
		for i, (lin3, col3) in reversed(list(enumerate(output))):
			if self.grid[lin3][col3] == -1:
			 	output.pop(i)
		return output

	def get_reward(self, lin, col):
		"""
			Retourne la recompence pour l'etat donne en parametre
		"""
		output = 0
		if lin == self.grid.shape[0]-1 and col == self.grid.shape[1]-1:
			output = 1000
		else:
			output = -self.weight[self.grid[lin, col]]
		return output

	def get_S(self):
		"""
			retourne une liste des coordonnees de tous les etats possible
		"""
		output = []
		for lin in range(self.grid.shape[0]):
			for col in range(self.grid.shape[1]):
				if self.grid[lin][col] != -1:
					output.append((lin, col))
		return output

	def _get_neighborhood(self, lin, col):
		"""
			Retourne une liste de coordonnees, ceulin des etats voisins de l'etat de coordonnees lin col
		"""
		output = [(action, (lin+lin2, col+col2)) for lin2 in [-2, -1, 1, 2] for col2 in [-2, -1, 1, 2] for action in ['Y', 'U', 'J', 'H', 'G', 'F', 'R', 'T'] if (lin+lin2 >= 0 and col+col2 >= 0 and lin+lin2 < len(self.grid) and col+col2 < len(self.grid[0])) and ((action == 'col' and lin2 == -2 and col2 == 1) or (action == 'U' and lin2 == -1 and col2 == 2) or (action == 'J' and lin2 == 1 and col2 == 2) or (action == 'H' and lin2 == 2 and col2 == 1) or (action == 'G' and lin2 == 2 and col2 == -1) or (action == 'F' and lin2 == 1 and col2 == -2) or (action == 'R' and lin2 == -1 and col2 == -2) or (action == 'T' and lin2 == -2 and col2 == -1))]

		for i, (action, (lin3, col3)) in reversed(list(enumerate(output))):
			if self.grid[lin3][col3] == -1:
			 	output.pop(i)

		return output
