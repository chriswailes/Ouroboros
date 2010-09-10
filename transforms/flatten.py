"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/09/01
Description:	A transformation that flattens the provided AST.
"""

from lib.ast import *
from lib import util
from lib.variables import v

def flatten(node, inplace = False):
	if isinstance(node, Assign):
		preStmts, node.exp = flatten(node.exp, True)
		
		return preStmts, node
	
	elif isinstance(node, BinOp):
		leftPreStmts, node.left = flatten(node.left)
		rightPreStmts, node.right = flatten(node.right)
		
		preStmts = util.flatten([leftPreStmts, rightPreStmts])
		
		if inplace:
			return preStmts, node
		else:
			var = v.getVar()
			preStmts.append(Assign(var, node))
			return preStmts, var
	
	elif isinstance(node, FunctionCall):
		preStmts = []
		newArgs = []
		
		for arg in node.args:
			tmpPreStmts, newArg = flatten(arg)
			
			preStmts.append(tmpPreStmts)
			newArgs.append(newArg)
		
		preStmts = util.flatten(preStmts)
		node.args = newArgs
		
		if inplace:
			return preStmts, node
		else:
			var = v.getVar()
			preStmts.append(Assign(var, node))
			return preStmts, var
	
	elif isinstance(node, Integer):
		return [], node
	
	elif isinstance(node, Module):
		newStmts = []
		
		for s in node.stmts:
			preStmts, newStmt = flatten(s, True)
			
			newStmts.append(preStmts)
			newStmts.append(newStmt)
		
		node.stmts = util.flatten(newStmts)
		return node
	
	elif isinstance(node, Name):
		return [], node
	
	elif isinstance(node, UnaryOp):
		preStmts, node.operand = flatten(node.operand)
		
		if inplace:
			return util.flatten(preStmts), node
		else:
			var = v.getVar()
			preStmts.append(Assign(var, node))
			return util.flatten(preStmts), var

