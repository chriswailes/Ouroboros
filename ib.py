"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/08/26
Description:	Classes and functions for building instructions.
"""

import myAST
import util

class Block(object):
	def __init__(self, header = ""):
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
		if (self.pos + 1) < self.getNumInsts():
			return self.getInst(self.pos + 1)
		else:
			return None
	
	def getNumInsts(self):
		num = 0
		
		for i in self.insts:
			if isinstance(i, Block):
				num += i.getNumInsts()
			else:
				num += 1
		
		return num
	
	def hasNext(self):
		return self.pos < (self.getNumInsts() - 1)
	
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

