"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/09/03
Description:	Removes expressions whos values aren't stored.
"""

from lib.ast import *
from lib.util import classGuard, extractSymbol, flatten

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
				sym = extractSymbol(child)
				
				#Throw out variables that are never read.
				if sym['reads'] != 0:
					newChildren.append(child)
			
			#If it is a Statement or a FunctionCall we need to keep the child.
			elif classGuard(child, Class, Function, FunctionCall, Statement):
				newChildren.append(child)
			
			elif isinstance(child, BasicBlock):
				#We can discard the nested BasicBlock.
				newChildren.append(discard(child).children)
			
			else:
				#Anything that reaches here is an expression outside of a
				#statement, and therefor has no effect on the program.
				#Therefor we remove any nested statements from the expression
				#then throw it away.
				newChildren.append(extractStmts(child))
		
		node.children = flatten(newChildren)
	
	else:
		for child in node:
			discard(child)
	
	return node

#Extracts statements from expressions and returns them.
def extractStmts(exp):
	stmts = []
	
	if classGuard(exp, BinOp, Dictionary, List, UnaryOp):
		for child in exp:
			if classGuard(child, Statement, FunctionCall):
				stmts.append(child)
			
			else:
				stmts.append(extractStmts(child))
	
	return flatten(stmts)
