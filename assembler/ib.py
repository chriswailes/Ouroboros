"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/08/26
Description:	General purpose classes and functions for building instructions.
"""

from lib import ast
from lib import util

class Block(object):
	def __init__(self, header = "\n"):
		self.header = header
		self.insts = []
		
		self.pos = 0
	
	def __str__(self):
		code = self.header
		
		for i in self.insts:
			code += str(i)
		
		return code

	def append(self, inst):
		self.insts.append(inst)
	
	def atEnd(self):
		return self.pos == self.getNumInsts()
	
	def getCurInst(self):
		if self.pos < self.getNumInsts():
			return self.getInst(self.pos)
		else:
			return None
		
	
	def getInst(self, index):
		localIndex, pos = self.getLocalIndex(index)
		
		if localIndex == None:
			return None
		else:
			o = self.insts[localIndex]
			if isinstance(o, Block):
				return o.getInst(pos)
			else:
				return o
	
	def getLocalIndex(self, index):
		localIndex = 0
		pos = 0
		
		if index < self.getNumInsts():
			for o in self.insts:
				if isinstance(o, Block):
					if pos <= index and index < (o.getNumInsts() + pos):
						pos = index - pos
						break
					else:
						pos += o.getNumInsts()
				elif pos == index:
					break
				else:
					pos += 1
				
				localIndex += 1
			
			return localIndex, pos
		else:
			return None, None
		
		
	
	def getNextInst(self):
		return self.lookahead()
	
	def getNumInsts(self):
		num = 0
		
		for i in self.insts:
			if isinstance(i, Block):
				num += i.getNumInsts()
			else:
				num += 1
		
		return num
	
	def hasNext(self):
		return (self.pos + 1) < self.getNumInsts()
	
	def lookahead(self, dist = 1):
		if (self.pos + dist) < self.getNumInsts():
			return self.getInst(self.pos + dist)
		else:
			return None
	
	def next(self):
		self.pos += 1
		return self.atEnd()
	
	def removeCurrent(self):
		self.removeInst(self.pos)
	
	def removeInst(self, index):
		localIndex, pos = self.getLocalIndex(index)
		
		if localIndex != None:
			o = self.insts[localIndex]
			if isinstance(o, Block):
				o.removeInst(pos)
			else:
				self.insts.pop(localIndex)
	
	def removeNextInst(self):
		self.removeInst(self.pos + 1)
	
	def reset(self):
		self.pos = 0

		for i in self.insts:
			if isinstance(i, Block):
				i.reset()

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
	def __init__(self, name, dest = None, suffix = "l", comment = ""):
		self.comment = comment
		self.name = name
		self.suffix = suffix
		
		if isinstance(dest, ast.Name):
			self.comment = "Var: " + dest.name
		
		self.dest = str(dest)
	
	def __str__(self):
		return self.pack("{0:5s} {1}".format(self.getOp(), self.dest))

class TwoOp(Instruction):
	def __init__(self, name, src = None, dest = None, suffix = "l", comment = ""):
		self.comment = comment
		self.name = name
		self.suffix = suffix
		
		self.src = str(src)
		
		self.dest = str(dest)
	
	def __str__(self):
		return self.pack("{0:5} {1}, {2}".format(self.getOp(), self.src, self.dest))

