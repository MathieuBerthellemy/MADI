from gurobipy import *
import numpy as np
import math

from Solver_PDM.SolverGurobi import *

class SolverGurobiPrimal(SolverGurobi):
	"""
		ATTRIBUTES
			- grid, np.matrix NxM
			- V
			- values
	"""
	def __init__(self, grid, weight):
		SolverGurobi.__init__(self, grid, weight)
		self.solve()


	def convert(self, vars):
		"""
			transforme la matrice des variables Gurobi en une matrice de char: la politique optimale
		"""
		output1 = np.chararray(self.grid.shape)
		output2 = np.zeros(self.grid.shape)
		last_value = 0
		for x in range(self.grid.shape[0]):
			for y in range(self.grid.shape[1]):
				if self.grid[x][y] == -1:
					output1[x][y] = '_'
					output2[x][y] = None
				else:
					output2[x][y] = self.V[x][y].x
					
					best_v = 0
					for action, (x_n, y_n) in self.get_neighborhood(x, y):
						if self.V[x_n][y_n].x > best_v:
							output1[x][y] = action
							best_v = self.V[x_n][y_n].x
				
							
		return output1, output2


	def set_constraints(self, model):
		self.set_constraint_main(model)
		model.update()
	
	def set_constraint_main(self, model):
		"""
			Ajoute la contrainte principale du PL
		"""
		for (x, y) in self.get_S():
			if x == self.grid.shape[0]-1 and y == self.grid.shape[1]-1:
				model.addConstr(self.V[self.grid.shape[0]-1][self.grid.shape[1]-1], GRB.EQUAL, 1000.0)
			else:
				neighborhood = self.get_neighborhood(x, y)
				for action, (x_n, y_n) in neighborhood:
					tmp = LinExpr()
					adjacents = self.get_adjacents(x_n, y_n)
					tmp.add(self.V[x_n][y_n], 1.0-(len(adjacents)/16.0))
					for (x2_n, y2_n) in adjacents:
						tmp.add(self.V[x2_n][y2_n], 1.0/16.0)
					
					model.addConstr(self.V[x][y], GRB.GREATER_EQUAL, self.get_R(x, y) + self.gamma * tmp, "(%d, %d)->(%d, %d)"%(x, y, x_n, y_n))

	
	

	def set_vars(self, model):
		"""
			Definit les variables du PL
		"""

		self.V = []
		
		for x in range(self.grid.shape[0]):
			self.V.append([])
			for y in range(self.grid.shape[1]):
				self.V[x].append([])
				if self.grid[x][y] != -1:
					self.V[x][y] = model.addVar(vtype=GRB.CONTINUOUS, name="V(%d, %d)"%(x, y))
				
		model.update()

	def set_objectif(self, model):
		"""
			Definit la fonction objectif du PL
		"""
		tmp = LinExpr()
		
		for x in range(self.grid.shape[0]):
			for y in range(self.grid.shape[1]):
				if self.grid[x][y] != -1:
					tmp.add(self.V[x][y], 1)

		model.setObjective(tmp, GRB.MINIMIZE)
		model.update()

