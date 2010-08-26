"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/08/26
Description:	Functions and data structures for allocating space on the stack
			for variables.
"""

import myAST

stackSize = 0
def getStackSize():
	global stackSize
	
	return stackSize

varNum = 0
varLocs = {}
def getVar():
	global stackSize
	global varLocs
	global varNum
	
	var = myAST.Name("tmp{0:d}".format(varNum))
	
	varNum += 1
	varLocs[var.name] = varNum * 4
	
	stackSize += 4
	
	return var

def getVarLoc(var):
	global stackSize
	global varLocs
	global varNum
	
	if varLocs.has_key(var):
		return varLocs[var]
	else:
		varNum += 1
		varLocs[var] = varNum * 4
		
		stackSize += 4
		
		return varLocs[var]
