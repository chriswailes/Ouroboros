"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/08/26
Description:	Functions and data structures for allocating space on the stack
			for variables.
"""

import ast

class VFile(object):
	def __init__(self, variables = {}):
		self.variables = variables.copy()
	
	def getVar(self, name = '!', increment = False):
		if self.variables.has_key(name):
			if increment:
				self.variables[name] += 1
		else:
			self.variables[name] = 0
		
		return "{0}:{1:d}".format(name, self.variables[name])
