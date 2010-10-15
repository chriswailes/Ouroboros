"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/10/12
Description:	Constants and functions for dealing with polymorphism.
"""

from assembler.ib import Immediate

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
