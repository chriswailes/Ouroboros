"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/08/26
Description:	Functions and data structures for allocating space on the stack
			for variables.
"""

import myAST

stackSize = 0
varNum = 0
varLocs = {}

def addUserVar(var):
	global stackSize
	global varLocs
	global varNum
	
	var = userName(var)
	
	if not varLocs.has_key(var):
		varNum += 1
		varLocs[var] = varNum * 4
		
		stackSize += 4
	
	return var

def getStackSize():
	global stackSize
	
	return stackSize

def getVar():
	global stackSize
	global varLocs
	global varNum
	
	var = myAST.Name("tmp:{0:d}".format(varNum))
	
	varNum += 1
	varLocs[var.name] = varNum * 4
	
	stackSize += 4
	
	return var

def getVarLoc(var):
	global varLocs
	
	return varLocs[var]

def userName(var):
	return "user:{0}".format(var)
