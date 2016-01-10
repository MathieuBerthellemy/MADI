from gurobipy import *
import numpy as np
import math

from Solver_PDM.SolverGurobi import *

class SolverGurobiDual(SolverGurobi):
	"""
		ATTRIBUTES
			- grid, np.matrix NxM
			- X
			- z
			- values
	"""

	

	def __init__(self, grid, weight, multiobjectif = True):
		self.multiobjectif = multiobjectif
		SolverGurobi.__init__(self, grid, weight)
		self.solve()


		

	def get_matrice_recompense_rouge(self):
		output = np.where(self.grid==3, 1, 0)
		output[self.grid.shape[0]-1, self.grid.shape[1]-1] = self.get_R(self.grid.shape[0]-1, self.grid.shape[1]-1)
		return output

	def get_matrice_recompense_bleu(self):
		output = np.where(self.grid==2, 1, 0)
		output[self.grid.shape[0]-1, self.grid.shape[1]-1] = self.get_R(self.grid.shape[0]-1, self.grid.shape[1]-1)
		return output



	def convert(self, vars):
		"""
			transforme la matrice des variables Gurobi en une matrice de char: la politique optimale
		"""
		output1 = np.chararray(self.grid.shape)
		output2 = np.zeros(self.grid.shape)
		last_value = 0
		for (x, y) in self.get_S():
			for key, value in self.D[x][y].items():
				if value.x == 1:
					output1[x, y] = key
					#output2[x, y] = self.X[x][y][key]
					break;
							
		return output1, output2


	def get_multiobjectif_expression(self, matrice):
		output = LinExpr()
		for (x, y) in self.get_S():
			# if x == self.grid.shape[0]-1 and y == self.grid.shape[1]-1:
			# 	pass
			# else:
			for action, (x_n, y_n) in self.get_neighborhood(x, y):
				adjacents = self.get_adjacents(x_n, y_n)
				tmp = -2 
				tmp += matrice[x_n, y_n] * (1 - len(adjacents)/16.0)
				#print "(", x, y, ")", matrice[x_n, y_n], "*", (1 - len(adjacents)/16.0), "=", tmp, action
				for (x_a, y_a) in adjacents:
					tmp += 1/16.0 * matrice[x_a, y_a]
				output.add(self.X[x][y][action], tmp)
		return output





	def set_vars(self, model):
		"""
			z: 
			X: 
		"""
		self.z = model.addVar(vtype=GRB.CONTINUOUS, lb=-99999999, name="z")
		self.X = [[{} for x in range(self.grid.shape[1])] for y in range(self.grid.shape[0])]
		self.D = [[{} for x in range(self.grid.shape[1])] for y in range(self.grid.shape[0])]
		
		for (x, y) in self.get_S():
			for action in self.get_all_action():
				self.X[x][y][action] = model.addVar(vtype=GRB.CONTINUOUS, lb=0.0, ub=1, name="X(%d,%d)<-(%s)"%(x, y, action))

		for (x, y) in self.get_S():
			for action in self.get_all_action():
				self.D[x][y][action] = model.addVar(vtype=GRB.BINARY, name="D(%d,%d)<-(%s)"%(x, y, action))


		model.update()

	def set_constraints(self, model):
		if self.multiobjectif:
			self.set_constraint_linearisation(model)

		self.set_constraint_main(model)
		self.set_constraints_d(model)
		model.update()

	def set_constraints_d(self, model):

		for (x, y) in self.get_S():
			model.addConstr(sum(self.D[x][y].values()), GRB.EQUAL, 1.0)

		for (x, y) in self.get_S():
			for action, (x_n, y_n) in self.get_neighborhood(x, y):
				model.addConstr((1-self.gamma)*self.X[x][y][action], GRB.LESS_EQUAL, self.D[x][y][action])


	def set_constraint_main(self, model):
		for (x, y) in self.get_S():
			tmp = LinExpr()
			for action, (x_n, y_n) in self.get_neighborhood(x, y):
				tmp.add(self.X[x][y][action], 1.0)

			tmp2 = LinExpr()
			for action, (x_n, y_n) in self.get_neighborhood(x, y):
				adjacents = self.get_adjacents(x_n, y_n)
				proba = (1-len(adjacents)/16.0)
				tmp2.add(self.X[x_n][y_n][action], proba)
				for (x_a, y_a) in adjacents:
					tmp2.add(self.X[x_a][y_a][action], 1/16.0)

			tmp.add(tmp2, -self.gamma)

			model.addConstr(tmp, GRB.EQUAL, 1/2.0)
		
	def set_constraint_linearisation(self, model):
		tmp_blue = self.get_multiobjectif_expression(self.get_matrice_recompense_bleu())
		tmp_red = self.get_multiobjectif_expression(self.get_matrice_recompense_rouge())
				
		model.addConstr(tmp_blue, GRB.GREATER_EQUAL, self.z)
		model.addConstr(tmp_red, GRB.GREATER_EQUAL, self.z)

	def set_objectif(self, model):
		if self.multiobjectif:
			self.set_objectif_multi_objectif(model)
		else:
			self.set_objectif_mono_objectif(model)

	def set_objectif_multi_objectif(self, model):
		model.setObjective(self.z, GRB.MAXIMIZE)
		model.update()

	def set_objectif_mono_objectif(self, model):
		tmp_blue = self.get_multiobjectif_expression(self.get_matrice_recompense_bleu())
		tmp_red = self.get_multiobjectif_expression(self.get_matrice_recompense_rouge())
		
		model.setObjective((tmp_red+tmp_blue)/2.0, GRB.MAXIMIZE)
		model.update()

