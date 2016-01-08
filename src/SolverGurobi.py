import numpy
import numpy as np
from gurobipy import *
import math

class SolverGurobi:
	"""
		ATTRIBUTES
			- grid, np.matrix NxM
			- V
			- solution
			- values
	"""
	def __init__(self, grid, alpha=0.5):
		self.alpha = alpha # part du but pour arriver a destination
		self.grid = grid
		self.width = len(grid)
		self.height = len(grid[0])
		self.gamma = min(self._compute_gamma(), 0.8)
		print self.gamma
		self._solve()


	def _compute_gamma(self):
		D = self.width+self.height

		output = 0.5
		output_bounds = (0, 1)

		window = (5, 10)
		while True:

			tmp = self._get_R(self.width-1, self.height-1)
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


	def get_move(self, x, y):
		return self.solution[x][y]

	def _solve(self):
		model = self._def_PL()
		model.write("pl.lp")
		model.optimize()
		self.solution, self.values = self._convert(model.getVars())
		

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

	def _convert(self, vars):

		output1 = np.chararray((self.width, self.height))
		output2 = np.zeros((self.width, self.height))
		last_value = 0
		for x in range(self.width):
			for y in range(self.height):
				if self.grid[x][y] == -1:
					output1[x][y] = '_'
					output2[x][y] = -1
				else:
					output2[x][y] = self.V[x][y].x
					
					best_v = 0
					for action, (x_n, y_n) in self._get_neighborhood(x, y):
						if self.V[x_n][y_n].x > best_v:
							output1[x][y] = action
							best_v = self.V[x_n][y_n].x
				
							
		return output1, output2

	def _get_R(self, x, y):
		output = -1
		if self._is_blue(x, y):
			output = -1
		elif self._is_red(x, y):
			output = -1
		elif x == self.width-1 and y == self.height-1:
			output = 998
		else:
			output = -2
		return output

	def _is_blue(self, x, y):
		return self.grid[x][y] == 2

	def _is_red(self, x, y):
		return self.grid[x][y] == 3

	def _get_neighborhood(self, x, y):
		output = [(action, (x+x2, y+y2)) for x2 in [-2, -1, 1, 2] for y2 in [-2, -1, 1, 2] for action in ['Y', 'U', 'J', 'H', 'G', 'F', 'R', 'T'] if (x+x2 >= 0 and y+y2 >= 0 and x+x2 < len(self.grid) and y+y2 < len(self.grid[0])) and ((action == 'Y' and x2 == -2 and y2 == 1) or (action == 'U' and x2 == -1 and y2 == 2) or (action == 'J' and x2 == 1 and y2 == 2) or (action == 'H' and x2 == 2 and y2 == 1) or (action == 'G' and x2 == 2 and y2 == -1) or (action == 'F' and x2 == 1 and y2 == -2) or (action == 'R' and x2 == -1 and y2 == -2) or (action == 'T' and x2 == -2 and y2 == -1))]

		for i, (action, (x3, y3)) in reversed(list(enumerate(output))):
			if self.grid[x3][y3] == -1:
			 	output.pop(i)

		return output

	def _get_adjacents(self, x, y):
		output = [(x+x2, y+y2) for x2 in [-1, 0, 1] for y2 in [-1, 0, 1] if (x+x2 >= 0 and y+y2 >= 0 and x+x2 < len(self.grid) and y+y2 < len(self.grid[0])) and not(x2 == 0 and y2 == 0)]
		for i, (x3, y3) in reversed(list(enumerate(output))):
			if self.grid[x3][y3] == -1:
			 	output.pop(i)

		return output

	def _def_PL(self):
		model = Model("MR")  
		z, self.V = self._get_vars(model)
		self._set_constraints(model, z)
		self._set_objectif(model, z)
		model.setParam('OutputFlag', False)
		return model

	def _set_constraint_end(self, model):
		model.addConstr(self.V[self.width-1][self.height-1], GRB.EQUAL, 1000)

	def _set_constraint_main(self, model):
		for (x, y) in self.get_S():
			neighborhood = self._get_neighborhood(x, y)
			for action, (x_n, y_n) in neighborhood:
				tmp = LinExpr()
				adjacents = self._get_adjacents(x_n, y_n)
				tmp.add(self.V[x_n][y_n], 1.0-(len(adjacents)/16.0))
				for (x2_n, y2_n) in adjacents:
					tmp.add(self.V[x2_n][y2_n], 1.0/16.0)
				
				model.addConstr(self.V[x][y], GRB.GREATER_EQUAL, self._get_R(x, y) + self.gamma * tmp)

	def _set_constraint_linearisation_max(self, model, z):
		tmp_blue = LinExpr();
		tmp_red = LinExpr();

		for x in range(self.width):
			for y in range(self.height):
				var = self.V[x][y]
				if self._is_blue(x, y):
					tmp_blue.add(var, 1.0)
				if self._is_red(x, y):
					tmp_red.add(var, 1.0)
				
		model.addConstr(tmp_blue, GRB.GREATER_EQUAL, z)
		model.addConstr(tmp_red, GRB.GREATER_EQUAL, z)

	def _set_constraints(self, model, z):
		self._set_constraint_main(model)
		self._set_constraint_linearisation_max(model, z)
		model.update()

	def _get_vars(self, model):
		"""
			z: INTEGER
			X: dictionary<var, tupple>, var -> GRB var, action
		"""

		z = model.addVar(vtype=GRB.CONTINUOUS, name="z")
		V = []
		
		for x in range(self.width):
			V.append([])
			for y in range(self.height):
				V[x].append([])
				if self.grid[x][y] != -1:
					V[x][y] = model.addVar(vtype=GRB.CONTINUOUS, name="V(%d, %d)"%(x, y))
				
		model.update()
		return z, V

	def _set_objectif(self, model, z):
		tmp = LinExpr()
		
		for x in range(self.width):
			for y in range(self.height):
				if self.grid[x][y] != -1:
					tmp.add(self.V[x][y], self.alpha)

		tmp.add(z, -(1-self.alpha))

		model.setObjective(tmp, GRB.MINIMIZE)
		model.update()

