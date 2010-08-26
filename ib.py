"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/08/26
Description:	Classes and functions for building instructions.
"""

import myAST

class Block(object):
	def __init__(self, header = ""):
		self.header = header
		self.insts = []
	
	def __str__(self):
		code = self.header
		
		for i in self.insts:
			code += str(i)
		
		return code

	def append(self, inst):
		self.insts.append(inst)

class Instruction(object):
	def __init__(self, name, suffix = None):
		self.name = name
		self.suffix = suffix
	
	def __str__(self):
		return self.bookend(self.getOp())
	
	def bookend(self, str):
		return "\t" + str + "\n"
	
	def getOp(self):
		if self.suffix == None:
			return self.name
		else:
			return self.name + self.suffix

class OneOp(Instruction):
	def __init__(self, name, op = None, suffix = "l"):
		self.name = name
		self.suffix = suffix
		
		self.op = op
	
	def __str__(self):
		return self.bookend(self.getOp() + " " + self.op)

class TwoOp(Instruction):
	def __init__(self, name, src = None, dest = None, suffix = "l"):
		self.name = name
		self.suffix = suffix
		
		self.src = src
		self.dest = dest
	
	def __str__(self):
		return self.bookend(self.getOp() + " " + str(self.src) + ", " + str(self.dest))

