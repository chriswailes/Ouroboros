"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/08/26
Description:	Functions and data structures for allocating space on the stack
			for variables.
"""

import ast


class VFile(object):
	def __init__(self):
		self.tmpCount = 0
		self.variables = []

	def getVar(self):
		self.tmpCount += 1
		
		var = ast.Name("tmp:{0:d}".format(self.tmpCount))
		self.variables.append(var)
		
		return var

	def userVar(self, var):
		var = "user:{0}".format(var)
		
		if not var in self.variables:
			self.variables.append(var)
		
		return var

v = VFile()
