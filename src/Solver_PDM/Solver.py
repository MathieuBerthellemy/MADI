import numpy as np
import math 

class Solver:

	def __init__(self, grid, weight):
		self.grid = grid
		self.weight = weight
		self.gamma =  self.compute_gamma(grid.shape[0], grid.shape[1], 1000)
		#self.gamma = 0.7
		self.solution = np.chararray(grid.shape)


	def get_neighborhood(self, x, y):
		output = [(action, (x+x2, y+y2)) for x2 in [-2, -1, 1, 2] for y2 in [-2, -1, 1, 2] for action in ['Y', 'U', 'J', 'H', 'G', 'F', 'R', 'T'] if (x+x2 >= 0 and y+y2 >= 0 and x+x2 < len(self.grid) and y+y2 < len(self.grid[0])) and ((action == 'Y' and x2 == -2 and y2 == 1) or (action == 'U' and x2 == -1 and y2 == 2) or (action == 'J' and x2 == 1 and y2 == 2) or (action == 'H' and x2 == 2 and y2 == 1) or (action == 'G' and x2 == 2 and y2 == -1) or (action == 'F' and x2 == 1 and y2 == -2) or (action == 'R' and x2 == -1 and y2 == -2) or (action == 'T' and x2 == -2 and y2 == -1))]

		for i, (action, (x3, y3)) in reversed(list(enumerate(output))):
			if self.grid[x3][y3] == -1:
			 	output.pop(i)

		return output

	def get_adjacents(self, x, y):
		output = [(x+x2, y+y2) for x2 in [-1, 0, 1] for y2 in [-1, 0, 1] if (x+x2 >= 0 and y+y2 >= 0 and x+x2 < len(self.grid) and y+y2 < len(self.grid[0])) and not(x2 == 0 and y2 == 0)]
		for i, (x3, y3) in reversed(list(enumerate(output))):
			if self.grid[x3][y3] == -1:
			 	output.pop(i)

		return output

	def get_R(self, x, y):
		return self.weight[self.grid[x, y]]

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

	def get_move(self, x, y):
		return self.solution[x][y]


	def get_all_action(self):
		return ['Y', 'U', 'J', 'H', 'G', 'F', 'R', 'T']


	def compute_gamma(self, width, height, R):
		D = width+height

		output = 0.5
		output_bounds = (0, 1)

		window = (5, 10)
		while True:

			tmp = R
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
		return min(output, 0.8)
