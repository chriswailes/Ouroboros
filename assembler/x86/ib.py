"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/08/26
Description:	Classes and functions for building x86 instructions.
"""

from assembler import ib
from assembler.ib import Block, Immediate, Instruction, Labeler, Label

from assembler.coloring import Mem, Register

from lib.ast import *

TAG_SIZE	= Immediate(2)
TAG_MASK	= Immediate(0x3)

INT_TAG	= Immediate(0x0)
BOOL_TAG	= Immediate(0x1)
OBJ_TAG	= Immediate(0x3)

FALS		= Immediate(0x1)
TRU		= Immediate(0x5)

class OneOp(ib.OneOp):
	def __init__(self, name, operand = None, suffix = "l", comment = ""):
		super(OneOp, self).__init__(name, operand, suffix, comment)

class TwoOp(ib.TwoOp):
	def __init__(self, name, src = None, dest = None, suffix = "l", comment = ""):
		if isinstance(src, Mem) and isinstance(dest, Mem):
			raise Exception("Both operands are memory locations.")
		
		super(TwoOp, self).__init__(name, src, dest, suffix, comment)

def getTempColor(cf, node, *interference):
	interference = node['pre-alive'] | set(interference)
	tmpColor = cf.getColor(interference, Register)
	
	if tmpColor == None:
		raise Spill(node['pre-alive'])
	
	else:
		return tmpColor

def restoreRegs(code, regs, inUse):
	regs.reverse()
	
	for reg in regs:
		if reg in inUse:
			code.append(OneOp('pop', reg))

def saveRegs(code, regs, inUse):
	for reg in regs:
		if reg in inUse:
			code.append(OneOp('push', reg))

def pack(imm, typ):
	global TAG_SIZE
	
	if isinstance(imm, Immediate):
		if typ == Integer:
			value = imm.value << TAG_SIZE.value
		
		else:
			raise Exception('Unspported object in pack funcion.')
		
		return Immediate(value)
	
	else:
		raise Exception('Trying to pack a non-Value node.')

def unpack(imm):
	global TAG_SIZE
	
	if isinstance(imm, Immediate):
		return imm.value >> TAG_SIZE.value
	
	else:
		raise Exception('Trying to unpack a non-Immediate value.')

def tag(obj, typ):
	global TAG_SIZE, BOOL_TAG, OBJ_TAG
	
	if isinstance(obj, Register):
		code = Block('')
		
		code.append(TwoOp('sal', TAG_SIZE, obj))
		
		if typ == Integer:
			pass
		
		elif typ == Boolean:
			code.append(TwoOp('and', BOOL_TAG, obj))
		
		else:
			code.append(TwoOp('and', OBJ_TAG, obj))
		
		return code
	
	else:
		raise Exception('Trying to tag a value that isn\'t a register.')

def untag(reg):
	return TwoOp('sar', TAG_SIZE, reg)
