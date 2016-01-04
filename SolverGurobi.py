import numpy
import numpy as np
from gurobipy import *

class SolverGurobi:
	"""
		ATTRIBUTES
			- grid, np.matrix NxM
			- X
			- solution
	"""
	def __init__(self, grid):
		self.gamma = 0.7
		self.grid = grid
		self._solve()

	def print_solution(self):
		print self.solution

	def get_move(self, x, y):
		return self.solution[x][y]

	def _solve(self):
		model = self._def_PL()
		model.write("pl.lp")
		model.optimize()
		self.solution = self.convert(model.getVars())
		

	def convert(self, vars):
		width = len(self.grid)
		height = len(self.grid[0])

		output = np.chararray((width, height))

		for x in range(width):
			for y in range(height):	
				best_v = 0
				for action, (x_n, y_n) in self._get_neighborhood(x, y):
					if self.V[x_n][y_n].x > best_v:
						if self.grid[x][y] == -1:
							output[x][y] = '_'
						else:
							output[x][y] = action
		return output

	def _get_R(self, x, y):
		width = len(self.grid)
		height = len(self.grid[0])
		output = -1
		if self._is_blue(x, y):
			output = -1
		elif self._is_red(x, y):
			output = -1
		elif x == width-1 and y == height-1:
			output = 1000
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
		width = len(self.grid)
		height = len(self.grid[0])
		model.addConstr(self.V[width-1][height-1], GRB.EQUAL, 1000)

	def _set_constraint_main(self, model):
		width = len(self.grid)
		height = len(self.grid[0])

		for x in range(width):
			for y in range(height):
				if x != width - 1 and y != height - 1:
					neighborhood = self._get_neighborhood(x, y)
					for action, (x_n, y_n) in neighborhood:
						tmp = LinExpr()
						tmp.add(self.V[x_n][y_n], 1.0-(len(neighborhood)/16.0))

						for (x2_n, y2_n) in self._get_adjacents(x_n, y_n):
							tmp.add(self.V[x2_n][y2_n], 1.0/16.0)
						
						model.addConstr(self.V[x][y], GRB.GREATER_EQUAL, self._get_R(x_n, y_n) + self.gamma * tmp)

	def _set_constraint_linearisation_max(self, model, z):
		tmp_blue = LinExpr();
		tmp_red = LinExpr();
		
		width = len(self.grid)
		height = len(self.grid[0])

		for x in range(width):
			for y in range(height):
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
		self._set_constraint_end(model)
		model.update()

	def _get_vars(self, model):
		"""
			z: INTEGER
			X: dictionary<var, tupple>, var -> GRB var, action
		"""
		width = len(self.grid)
		height = len(self.grid[0])

		z = model.addVar(vtype=GRB.CONTINUOUS, name="z")
		V = []
		
		for x in range(width):
			V.append([])
			for y in range(height):
				V[x].append([])
				V[x][y] = model.addVar(vtype=GRB.CONTINUOUS, name="V(%d, %d)"%(x, y))
				
		model.update()
		return z, V

	def _set_objectif(self, model, z):
		tmp = LinExpr()
		width = len(self.grid)
		height = len(self.grid[0])
		
		for x in range(width):
			for y in range(height):
				tmp.add(self.V[x][y], 1.0)

		tmp.add(z, 1.0)

		model.setObjective(tmp, GRB.MINIMIZE)
		model.update()

