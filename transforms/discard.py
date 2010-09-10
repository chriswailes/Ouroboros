"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/09/03
Description:	Removes expressions whos values aren't stored.
"""

from lib import ast
from lib import util

def discard(node):
	if isinstance(node, ast.Assign):
		return node
	
	elif isinstance(node, ast.BasicBlock):
		newChildren = []
		
		for child in node:
			if isinstance(child, ast.FunctionCall) or isinstance(child, ast.Statement):
				newChildren.append(child)
			else:
				newChildren.append(extractStmts(child))
		
		node.children = util.flatten(newChildren)
		return node
			
	elif isinstance(node, ast.BinOp):
		return node
	
	elif isinstance(node, ast.FunctionCall):
		return node
	
	elif isinstance(node, ast.If):
		node.then = discard(node.then)
		node.els = discard(node.els)
		
		return node
	
	elif isinstance(node, ast.Integer):
		return node
	
	elif isinstance(node, ast.Module):
		node.block = discard(node.block)
		
		return node
	
	elif isinstance(node, ast.Name):
		return node
	
	elif isinstance(node, ast.UnaryOp):
		return node

def extractStmts(exp):
	if isinstance(exp, ast.BinOp):
		stmts = []
		
		if isinstance(exp.left, ast.FunctionCall) or isinstance(exp.left, ast.Statement):
			stmts.append(exp.left)
		else:
			stmts.append(extractStmts(exp.left))
		
		if isinstance(exp.right, ast.FunctionCall) or isinstance(exp.right, ast.Statement):
			stmts.append(exp.right)
		else:
			stmts.append(extractStmts(exp.right))
		
		return util.flatten(stmts)
	
	elif isinstance(exp, ast.Integer):
		return []
	
	elif isinstance(exp, ast.Name):
		return []
	
	elif isinstance(exp, ast.UnaryOp):
		if isinstance(exp.operand, ast.FunctionCall) or isinstance(exp.operand, ast.Statement):
			return [exp.operand]
		else:
			return util.flatten(extractStmts(exp.operand))
