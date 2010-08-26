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
	def __init__(self, name, suffix = None, comment = ""):
		self.comment = comment
		self.name = name
		self.suffix = suffix
	
	def __str__(self):
		return self.pack(self.getOp())
	
	def getOp(self):
		if self.suffix == None:
			return self.name
		else:
			return self.name + self.suffix
	
	def pack(self, instr):
		return "\t{0:21} # {1}\n".format(instr, self.comment)

class OneOp(Instruction):
	def __init__(self, name, operand = None, suffix = "l", comment = ""):
		self.comment = comment
		self.name = name
		self.suffix = suffix
		
		if isinstance(operand, myAST.Name):
			self.comment = "Var: " + operand.name
		
		self.operand = str(operand)
	
	def __str__(self):
		return self.pack("{0:5s} {1}".format(self.getOp(), self.operand))

class TwoOp(Instruction):
	def __init__(self, name, src = None, dest = None, suffix = "l", comment = ""):
		self.comment = comment
		self.name = name
		self.suffix = suffix
		
		self.src = str(src)
		
		if isinstance(dest, myAST.Name):
			self.comment = "Var: " + dest.name
		self.dest = str(dest)
	
	def __str__(self):
		return self.pack("{0:5} {1}, {2}".format(self.getOp(), str(self.src), str(self.dest)))

