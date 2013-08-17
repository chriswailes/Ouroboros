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
	newChildren = []
	
	for child in node:
		newChild = eliminateDeadCode(child)
		
		if isinstance(node, BasicBlock):
			if classGuard(newChild, Class, Function, FunctionCall, SetAttr, Statement):
				newChildren.append(newChild)
			
			elif isinstance(newChild, BasicBlock):
				newChildren.append(newChild.children)
			
			elif isinstance(newChild, Return):
				newChildren.append(newChild)
				
				# All nodes after the Return node will be discarded due to
				# unreachability.
				break
			
			else:
				# Anything that reaches here is an expression outside of a
				# statement, and therefor has no effect on the program.
				# Therefor we remove any nested statements from the
				# expression then throw it away.
				newChildren.append(extractStmts(newChild))
		
		else:
			newChildren.append(newChild)
	
	node.setChildren(flatten(newChildren))
	
	if classGuard(node, If, IfExp) and isinstance(node.cond, Literal):
		# If statements or expressions with a literal conditional value can
		# be eliminated and replaced with the appropriate BasicBlock's
		# children.
			
		return node.then if node.cond.value else node.els
	
	else:
		return node

# Extracts statements from expressions and returns them.
def extractStmts(exp):
	stmts = []
	
	if classGuard(exp, BinOp, Dictionary, List, UnaryOp):
		for child in exp:
			if classGuard(child, Statement, FunctionCall):
				stmts.append(child)
			
			else:
				stmts.append(extractStmts(child))
	
	return flatten(stmts)
