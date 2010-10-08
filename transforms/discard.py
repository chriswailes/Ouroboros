"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/09/03
Description:	Removes expressions whos values aren't stored.
"""

from lib.ast import *
from lib.util import flatten, classGuard

analysis	= ['reads']
args		= []

def init():
	from transforms.pass_manager import register
	register('discard', discard, analysis, args)

def discard(node):
	if isinstance(node, BasicBlock):
		newChildren = []
		
		for child in node:
			if isinstance(child, Assign):
				sym = child.var.symbol if isinstance(child, Subscript) else child.var
				
				#Throw out variables that are never read.
				if sym['reads'] != 0:
					newChildren.append(child)
			
			#If it is a Statement or a FunctionCall we need to keep the child.
			elif classGuard(child, Statement, FunctionCall):
				newChildren.append(child)
			
			#Anything that reaches here is an expression outside of a
			#statement, and therefor has no effect on the program.  Therefor
			#we remove any nested statements from the expression then throw
			#it away.
			else:
				newChildren.append(extractStmts(child))
		
		node.children = flatten(newChildren)
	
	else:
		for child in node:
			discard(child)
	
	return node

#Extracts statements from expressions and returns them.
def extractStmts(exp):
	stmts = []
	
	if isinstance(exp, BinOp):
		if classGuard(exp.left, Statement, FunctionCall):
			stmts.append(exp.left)
		else:
			stmts.append(extractStmts(exp.left))
		
		if classGuard(exp.right, Statement, FunctionCall):
			stmts.append(exp.right)
		else:
			stmts.append(extractStmts(exp.right))
	
	elif classGuard(exp, List, Dictionary):
		for child in exp:
			if classGuard(child, Statement, FunctionCall):
				stmts.append(child)
			
			else:
				stmts.append(extractStmts(child))
	
	elif isinstance(exp, UnaryOp):
		if classGuard(exp.operand, Statement, FunctionCall):
			stmts.append(exp.operand)
		else:
			stmts.append(extractStmts(exp.operand))
	
	return flatten(stmts)
