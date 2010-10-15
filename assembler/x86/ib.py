"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/08/26
Description:	Classes and functions for building x86 instructions.
"""

from assembler import *
from assembler.coloring import Mem, Register
from assembler.ib import Block, Immediate, Instruction, Labeler, Label
from assembler.tagging import *

labeler = Labeler()

class OneOp(ib.OneOp):
	def __init__(self, name, operand = None, suffix = "l", comment = ""):
		super(OneOp, self).__init__(name, operand, suffix, comment)

class TwoOp(ib.TwoOp):
	def __init__(self, name, src = None, dest = None, suffix = "l", comment = ""):
		if isinstance(src, Mem) and isinstance(dest, Mem):
			raise Exception("Both operands are memory locations.")
		
		super(TwoOp, self).__init__(name, src, dest, suffix, comment)

def getTmpColor(cf, node, *interference):
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

def buildITE(cond, then, els, comp = Immediate(0), jmp = 'jz', test = False):
	global labeler
	
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

def move(src, dest):
	if isinstance(src, Immediate):
		dest.tagged = src.packed
	
	else:
		dest.tagged = src.tagged
	
	return TwoOp('mov', src, dest)
	
def tag(obj, typ = None):
	global INT, BOOL, TAG_SIZE, BOOL_TAG, OBJ_TAG
	
	if isinstance(obj, Register):
		code = Block('')
		
		if typ:
			obj.tagged = False
			obj.tag = typ
		
		if not obj.tagged:
			if obj.tag == INT:
				code.append(TwoOp('sal', TAG_SIZE, obj))
			
			elif obj.tag == BOOL:
				code.append(TwoOp('sal', TAG_SIZE, obj))
				code.append(TwoOp('or', BOOL_TAG, obj))
			
			elif obj.tag == OBJ:
				code.append(TwoOp('or', OBJ_TAG, obj))
			
			obj.tagged = True
		
		return code
	
	else:
		raise Exception("Trying to tag a value that isn't in a register.")

def untag(reg):
	global TAG_SIZE
	
	if isinstance(reg, Register):
		if reg.tagged:
			reg.tagged = False
			return TwoOp('sar', TAG_SIZE, reg)
	
	else:
		raise Exception("Trying to untag a value that isn't in a register.")

def getTag(reg):
	global REST_MASK
	
	if isinstance(obj, Register):
		reg.tagged = False
		return TwoOp('and', REST_MASK, reg)
	
	else:
		raise Exception("Trying to get the tag of a value that isn't in a register.")
