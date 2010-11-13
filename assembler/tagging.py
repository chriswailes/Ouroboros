"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/10/12
Description:	Constants and functions for dealing with polymorphism.
"""

from assembler.coloring import Mem, Register
from assembler.ib import Block, Immediate, Labeler

from lib.config import config
from lib.util import Enum

#################
# Tag Type Enum #
#################

INT	= Enum(0)
BOOL	= Enum(1)
OBJ	= Enum(2)

#############################
# Literal Tagging Functions #
#############################

def pack(imm, typ):
	global TAG_SIZE
	
	if isinstance(imm, int):
		imm = Immediate(imm)
	
	if isinstance(imm, Immediate):
		if not imm.packed:
			if typ == INT:
				imm.value <<= TAG_SIZE.value
			
			elif typ == BOOL:
				imm.value <<= TAG_SIZE.value
				imm.value  |= BOOL_TAG.value
			
			else:
				raise Exception('Unspported object type in pack funcion.')
		
			imm.packed = True
		
		return imm
	
	else:
		raise Exception('Trying to pack a non-Value node.')

def unpack(imm):
	global TAG_SIZE
	
	if isinstance(imm, Immediate):
		imm.packed = False
		return imm.value >> TAG_SIZE.value
	
	else:
		raise Exception('Trying to unpack a non-Immediate value.')

#################
# Tag Constants #
#################

TAG_SIZE	= Immediate(2)
TAG_MASK	= Immediate(0x3)
REST_MASK	= Immediate(~0x3)

INT_TAG	= Immediate(0x0)
BOOL_TAG	= Immediate(0x1)
OBJ_TAG	= Immediate(0x3)

TRU		= pack(0x1, BOOL)
FALS		= pack(0x0, BOOL)

###########################
# Color Tagging Functions #
###########################
	
def tag(obj, typ = None):
	global INT, BOOL, TAG_SIZE, BOOL_TAG, OBJ_TAG
	
	if config.arch == 'x86':
		from assembler.x86.ib import TwoOp, OneOp
	
	elif config.arch == 'x86_64':
		from assembler.x86_64.ib import TwoOp, OneOp
	
	if isinstance(obj, Register):
		code = Block('')
		
		if typ and obj.tag != typ:
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

def untag(reg, typ = INT):
	global TAG_SIZE, REST_MASK
	
	if config.arch == 'x86':
		from assembler.x86.ib import TwoOp, OneOp
	
	elif config.arch == 'x86_64':
		from assembler.x86_64.ib import TwoOp, OneOp
	
	if isinstance(reg, Register):
		if reg.tagged:
			reg.tagged = False
			
			if typ == OBJ:
				return TwoOp('and', REST_MASK, reg)
			
			else:
				return TwoOp('sar', TAG_SIZE, reg)
	
	else:
		raise Exception("Trying to untag a value that isn't in a register.")

def getTag(reg):
	global REST_MASK
	
	if config.arch == 'x86':
		from assembler.x86.ib import TwoOp, OneOp
	
	elif config.arch == 'x86_64':
		from assembler.x86_64.ib import TwoOp, OneOp
	
	if isinstance(obj, Register):
		reg.tagged = False
		return TwoOp('and', REST_MASK, reg)
	
	else:
		raise Exception("Trying to get the tag of a value that isn't in a register.")

