from gurobipy import Model
from Solver_PDM.Solver import *

class SolverGurobi(Solver):
	def __init__(self, grid, weight):
		Solver.__init__(self, grid, weight)


	def solve(self):
		"""
			Resoud le PL
		"""
		model = self.def_PL()
		model.write("pl.lp")
		model.optimize()
		print model.status
		self.solution, self.values = self.convert(model.getVars())


	def def_PL(self):
		"""
			Definie le PL, variables/contraintes/objectifs
		"""
		model = Model("MR")  
		self.set_vars(model)
		self.set_constraints(model)
		self.set_objectif(model)
		model.setParam('OutputFlag', False)
		return model

