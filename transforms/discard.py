"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/09/03
Description:	Removes expressions whos values aren't stored.
"""

from lib import ast
from lib import util

analysis	= ['reads']
args		= []

def init():
	from transforms.pass_manager import register
	register('discard', discard, analysis, args)

def discard(node):
	if isinstance(node, ast.BasicBlock):
		newChildren = []
		
		for child in node:
			if isinstance(child, ast.Assign):
				if isinstance(child.var, ast.Name):
					sym = child.var.symbol
				else:
					sym = child.var.name.symbol
				
				if sym['reads'] != 0:
					newChildren.append(child)
			
			elif isinstance(child, ast.FunctionCall) or isinstance(child, ast.Statement):
				newChildren.append(child)
			
			else:
				newChildren.append(extractStmts(child))
		
		node.children = util.flatten(newChildren)
	
	else:
		for child in node:
			discard(child)
	
	return node

def extractStmts(exp):
	stmts = []
	
	if isinstance(exp, ast.BinOp):
		if isinstance(exp.left, ast.FunctionCall) or isinstance(exp.left, ast.Statement):
			stmts.append(exp.left)
		else:
			stmts.append(extractStmts(exp.left))
		
		if isinstance(exp.right, ast.FunctionCall) or isinstance(exp.right, ast.Statement):
			stmts.append(exp.right)
		else:
			stmts.append(extractStmts(exp.right))
	
	elif isinstance(exp, ast.Dictionary) or  isinstance(exp, ast.List):
		for child in exp:
			if isinstance(child, ast.FunctionCall) or isinstance(child, ast.Statement):
				stmts.append(child)
			
			else:
				stmts.append(extractStmts(child))
	
	elif isinstance(exp, ast.UnaryOp):
		if isinstance(exp.operand, ast.FunctionCall) or isinstance(exp.operand, ast.Statement):
			stmts.append(exp.operand)
		else:
			stmts.append(extractStmts(exp.operand))
	
	return util.flatten(stmts)
