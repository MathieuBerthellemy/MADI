import numpy
import numpy as np
from gurobipy import *

class SolverGurobi:
	"""
		ATTRIBUTES
			- grid, np.matrix NxM
			- X
	"""
	def __init__(self, grid):
		self.grid = grid

	def get_solution(self):
		model = self._def_PL()
		model.write("pl.lp")
		model.optimize()
		return self.convert(model.getVars())
		

	def convert(self, vars):
		width = len(self.grid)
		height = len(self.grid[0])

		output = np.chararray((width, height))

		for x in range(width):
			for y in range(height):	
				for var, move, neighboor in self.X[x][y]:
					if var.x == 1:
						if self.grid[x][y] == -1:
							output[x][y] = '_'
						else:
							output[x][y] = move
						break
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

		z, self.X = self._get_vars(model)
		self._set_constraints(model, z)
		self._set_objectif(model, z)
		model.setParam('OutputFlag', False)
		return model

	def _set_constraint_sum_neightboor_eq_un(self, model):
		width = len(self.grid)
		height = len(self.grid[0])

		for x in range(width):
			for y in range(height):
				tmp = sum([var for var, move, neighboor in self.X[x][y]])
				if len(self.X[x][y]) > 0:
					model.addConstr(tmp, GRB.EQUAL, 1.0)

	def _set_constraint_linearisation_max(self, model, z):
		tmp_blue = LinExpr();
		tmp_red = LinExpr();
		
		width = len(self.grid)
		height = len(self.grid[0])

		for x in range(width):
			for y in range(height):
				nb_voisin = len(self.X[x][y])

				for var, move, (x_n, y_n) in self.X[x][y]:
					if self._is_blue(x_n, y_n):
						tmp_blue.add(var, 1.0-(nb_voisin/16.0))
					if self._is_red(x_n, y_n):
						tmp_red.add(var, 1.0-(nb_voisin/16.0))

				for var, move, (x_n, y_n) in self.X[x][y]:
					for (x_n, y_n) in self._get_adjacents(x_n, y_n):
						if self._is_blue(x_n, y_n):
							tmp_blue.add(var, 1.0/16.0)
						if self._is_red(x_n, y_n):
							tmp_red.add(var, 1.0/16.0)
				
		model.addConstr(tmp_blue, GRB.GREATER_EQUAL, z)
		model.addConstr(tmp_red, GRB.GREATER_EQUAL, z)



	def _set_constraints(self, model, z):
		self._set_constraint_sum_neightboor_eq_un(model)
		self._set_constraint_linearisation_max(model, z)
		model.update()

	def _get_vars(self, model):
		"""
			z: INTEGER
			X: dictionary<var, tupple>, var -> GRB var, action
		"""
		width = len(self.grid)
		height = len(self.grid[0])

		z = model.addVar(vtype=GRB.INTEGER, name="z")
		X = []
		
		for x in range(width):
			X.append([])
			for y in range(height):
				X[x].append([])
				X[x][y] = []
				for action, neighboor in self._get_neighborhood(x, y):
					var = model.addVar(vtype=GRB.BINARY, name="X(%d, %d);%s;(%d, %d)"%(x, y, action, neighboor[0], neighboor[1]))
					X[x][y].append((var, action, neighboor))

		model.update()
		return z, X

	def _set_objectif(self, model, z):
		tmp = LinExpr()
		width = len(self.grid)
		height = len(self.grid[0])
		
		# gain de but = 1000
		for (l, x, y) in [('H', width-2-1, height-1-1), ('J', width-1-1, height-2-1)]:
			for (var, move, o) in self.X[x][y]:
				if move == l:
					tmp.add(var, 1000.0)


		# Cout de mouvement = 2
		for x in range(width):
			for y in range(height):
				for  (var, move, o) in self.X[x][y]:
					tmp.add(var, -2.0)
		
		# esperance de gain bleu & rouge
		tmp.add(z, 1.0)

		model.setObjective(tmp, GRB.MAXIMIZE)
		model.update()

