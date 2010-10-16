"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/08/26
Description:	General purpose classes and functions for building instructions.
"""

from assembler import Spill
from assembler.coloring import Color, Mem, Register

from lib import ast
from lib.config import config
from lib.util import classGuard

###############################
# Instruction Builder Objects #
###############################

class Block(object):
	def __init__(self, header = "\n"):
		self.header = header
		self.insts = []
		
		self.pos = 0
	
	def __str__(self):
		code = self.header
		
		for i in self.insts:
			code += str(i)
			
			if isinstance(i, Label):
				code += ":\n"
		
		return code

	def append(self, inst):
		if (isinstance(inst, Block) and len(inst.insts) > 0) or classGuard(inst, Instruction, Label):
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

class Labeler(object):
	def __init__(self):
		self.cur = -1
	
	def nextLabel(self):
		self.cur += 1
		return Label(self.cur)

class Label(object):
	def __init__(self, num):
		self.num = num
		self.name = "L{0}".format(self.num)
	
	def __str__(self):
		return self.name

class Immediate(object):
	def __init__(self, value, packed = False):
		self.value = value
		self.packed = packed
	
	def __str__(self):
		return '$' + str(self.value)

class Instruction(object):
	def __init__(self, name, suffix = None, comment = ""):
		self.comment = comment
		self.name = name
		self.suffix = suffix
		
		self.pre_alive = []
		self.post_alive = []
	
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
	def __init__(self, name, operand = None, suffix = None, comment = ""):
		self.name = name
		self.suffix = suffix
		
		self.operand = operand
		
		if operand == None:
			raise Exception('None passed as operand to instruction.')
		
		self.comment = comment
	
	def __str__(self):
		return self.pack("{0:5s} {1}".format(self.getOp(), self.operand))

class TwoOp(Instruction):
	def __init__(self, name, src = None, dest = None, suffix = None, comment = ""):
		self.name = name
		self.suffix = suffix
		
		self.src = src
		self.dest = dest
		
		if src == None:
			raise Exception('None passed as src to instruction.')
		
		if dest == None:
			raise Exception('None passes as dest to instruction.')
		
		self.comment = comment
	
	def __str__(self):
		return self.pack("{0:5} {1}, {2}".format(self.getOp(), self.src, self.dest))

#################################
# Instruction Builder Functions #
#################################
labeler = Labeler()

def buildITE(cond, then, els, comp = Immediate(0), jmp = 'jz', test = False):
	global labeler
	
	if config.arch == 'x86':
		from assembler.x86.ib import TwoOp, OneOp
	
	elif config.arch == 'x86_64':
		from assembler.x86_64.ib import TwoOp, OneOp
	
	code = Block()
	
	endLabel = labeler.nextLabel()
	elsLabel = labeler.nextLabel() if els else endLabel
	
	if test:
		code.append(TwoOp('test', comp, cond))
	else:
		code.append(TwoOp('cmp', comp, cond))
	
	code.append(OneOp(jmp, elsLabel, None))
	
	#Now the then case
	code.append(then)
	code.append(OneOp('jmp', endLabel, None))
	
	if els:
		#Now the else label and case.
		code.append(elsLabel)
		code.append(els)
	
	code.append(endLabel)
	
	return code

def getTmpColor(cf, node, *interference):
	interference = node['pre-alive'] | set(interference)
	tmpColor = cf.getColor(interference, Register)
	
	if tmpColor == None:
		raise Spill(node['pre-alive'])
	
	else:
		return tmpColor

def move(src, dest):
	if config.arch == 'x86':
		from assembler.x86.ib import TwoOp, OneOp
	
	elif config.arch == 'x86_64':
		from assembler.x86_64.ib import TwoOp, OneOp
	
	if isinstance(src, Immediate):
		dest.tagged = src.packed
	
	else:
		dest.tagged = src.tagged
	
	return TwoOp('mov', src, dest)

def restoreRegs(code, regs, inUse):
	#Make a copy of the passed in list so we don't reverse it for everyone.
	regs = list(regs)
	regs.reverse()
	
	for reg in regs:
		if reg in inUse:
			code.append(OneOp('pop', reg))

def saveRegs(code, regs, inUse):
	for reg in regs:
		if reg in inUse:
			code.append(OneOp('push', reg))

