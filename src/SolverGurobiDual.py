import numpy
from tools import compute_gamma
import numpy as np
from gurobipy import *
import math

class SolverGurobiDual:
	"""
		ATTRIBUTES
			- grid, np.matrix NxM
			- X
			- z
			- solution
			- values
	"""

	def _get_all_action(self):
		return ['Y', 'U', 'J', 'H', 'G', 'F', 'R', 'T']

	def __init__(self, grid, weight):
		self.grid = grid
		self.weight = weight
		self.gamma =  compute_gamma(grid.shape[0], grid.shape[1], 1000)
		#self.gamma = 0.7
		print "gamma: ", self.gamma
		self._solve()


	def get_move(self, x, y):
		return self.solution[x][y]

	def _solve(self):
		model = self._def_PL()
		model.write("pl.lp")
		model.optimize()
		model.write("pl.sol")
		print model.status
		self.solution, self.values = self._convert(model.getVars())
		#print solution
		

	def _get_matrice_recompense_rouge(self):
		output = np.where(self.grid==3, 1, 0)
		output[self.grid.shape[0]-1, self.grid.shape[1]-1] = self._get_R(self.grid.shape[0]-1, self.grid.shape[1]-1)
		return output

	def _get_matrice_recompense_bleu(self):
		output = np.where(self.grid==2, 1, 0)
		output[self.grid.shape[0]-1, self.grid.shape[1]-1] = self._get_R(self.grid.shape[0]-1, self.grid.shape[1]-1)
		return output

	def _get_S(self):
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
		output1 = np.chararray(self.grid.shape)
		output2 = np.zeros(self.grid.shape)
		last_value = 0
		for (x, y) in self._get_S():
			for key, value in self.D[x][y].items():
				if value.x == 1:
					output1[x, y] = key
					#output2[x, y] = self.X[x][y][key]
					break;
							
		return output1, output2

	def _get_R(self, x, y):
		return self.weight[self.grid[x, y]]

	# def _is_blue(self, x, y):
	# 	return self.grid[x][y] == 2

	# def _is_red(self, x, y):
	# 	return self.grid[x][y] == 3

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
		self._set_vars(model)
		self._set_constraints(model)
		self._set_objectif(model)
		model.setParam('OutputFlag', False)
		return model


	def get_multiobjectif_expression(self, matrice):
		output = LinExpr()
		for (x, y) in self._get_S():
			# if x == self.grid.shape[0]-1 and y == self.grid.shape[1]-1:
			# 	pass
			# else:
			for action, (x_n, y_n) in self._get_neighborhood(x, y):
				adjacents = self._get_adjacents(x_n, y_n)
				tmp = -2 
				tmp += matrice[x_n, y_n] * (1 - len(adjacents)/16.0)
				#print "(", x, y, ")", matrice[x_n, y_n], "*", (1 - len(adjacents)/16.0), "=", tmp, action
				for (x_a, y_a) in adjacents:
					tmp += 1/16.0 * matrice[x_a, y_a]
				output.add(self.X[x][y][action], tmp)
		return output




	def _set_constraints(self, model):
		self._set_constraint_main(model)
		self._set_constraint_linearisation(model)
		self._set_constraints_d(model)
		model.update()

	def _set_constraints_d(self, model):

		for (x, y) in self._get_S():
			model.addConstr(sum(self.D[x][y].values()), GRB.EQUAL, 1.0)

		for (x, y) in self._get_S():
			for action, (x_n, y_n) in self._get_neighborhood(x, y):
				model.addConstr((1-self.gamma)*self.X[x][y][action], GRB.LESS_EQUAL, self.D[x][y][action])


	def _set_constraint_main(self, model):
		for (x, y) in self._get_S():
			tmp = LinExpr()
			for action, (x_n, y_n) in self._get_neighborhood(x, y):
				tmp.add(self.X[x][y][action], 1.0)

			tmp2 = LinExpr()
			for action, (x_n, y_n) in self._get_neighborhood(x, y):
				adjacents = self._get_adjacents(x_n, y_n)
				proba = (1-len(adjacents)/16.0)
				tmp2.add(self.X[x_n][y_n][action], proba)
				for (x_a, y_a) in adjacents:
					tmp2.add(self.X[x_a][y_a][action], 1/16.0)

			tmp.add(tmp2, -self.gamma)

			model.addConstr(tmp, GRB.EQUAL, 1/2.0)
		
	def _set_constraint_linearisation(self, model):
		tmp_blue = self.get_multiobjectif_expression(self._get_matrice_recompense_bleu())
		tmp_red = self.get_multiobjectif_expression(self._get_matrice_recompense_rouge())
				
		model.addConstr(tmp_blue, GRB.GREATER_EQUAL, self.z)
		model.addConstr(tmp_red, GRB.GREATER_EQUAL, self.z)

	def _set_vars(self, model):
		"""
			z: 
			X: 
		"""
		self.z = model.addVar(vtype=GRB.CONTINUOUS, lb=-99999999, name="z")
		self.X = [[{} for x in range(self.grid.shape[0])] for y in range(self.grid.shape[1])]
		self.D = [[{} for x in range(self.grid.shape[0])] for y in range(self.grid.shape[1])]
		
		for (x, y) in self._get_S():
			for action in self._get_all_action():
				self.X[x][y][action] = model.addVar(vtype=GRB.CONTINUOUS, lb=0.0, ub=1, name="X(%d,%d)<-(%s)"%(x, y, action))

		for (x, y) in self._get_S():
			for action in self._get_all_action():
				self.D[x][y][action] = model.addVar(vtype=GRB.BINARY, name="D(%d,%d)<-(%s)"%(x, y, action))


		model.update()


	def _set_objectif(self, model):
		tmp = LinExpr()
		model.setObjective(self.z, GRB.MAXIMIZE)
		model.update()

