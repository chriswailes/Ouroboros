"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		Ouroboros
Date:		2010/09/03
Description:	Removes expressions whos values aren't stored and branches whos
			conditional can be calculated at runtime..
"""

from lib.ast import *
from lib.util import classGuard, flatten

analysis	= []
args		= []

def init():
	from transforms.pass_manager import register
	register('dead_code', eliminateDeadCode, analysis, args)

def eliminateDeadCode(node):
	if isinstance(node, BasicBlock):
		newChildren = []
		
		for child in node:
			#If statements or expressions with a literal conditional value
			#can be eliminated and replaced with the appropriate BasicBlock's
			#children.
			if classGuard(child, If, IfExp) and isinstance(child.cond, Literal):
				block = child.then if child.cond.value else child.els
				newChildren.append(block.children)
			
			elif classGuard(child, Class, Function, FunctionCall, Statement):
				newChildren.append(child)
			
			elif isinstance(child, BasicBlock):
				#We can discard the nested BasicBlock.
				newChildren.append(eliminateDeadCode(child).children)
			
			elif isinstance(child, Return):
				newChildren.append(node)
				
				#All nodes after the Return node will be discarded due to
				#unreachability.
				break
			
			else:
				#Anything that reaches here is an expression outside of a
				#statement, and therefor has no effect on the program.
				#Therefor we remove any nested statements from the expression
				#then throw it away.
				newChildren.append(extractStmts(child))
		
		node.setChildren(flatten(newChildren))
	
	else:
		for child in node:
			eliminateDeadCode(child)
	
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
