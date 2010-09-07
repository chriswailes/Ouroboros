"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/09/03
Description:	Removes redundant negation expressions.
"""

from lib import ast
from lib import util

def redundantNegations(node):
	if isinstance(node, ast.Assign):
		node.exp = redundantNegations(node.exp)
		return node
			
	elif isinstance(node, ast.BinOp):
		node.left = redundantNegations(node.left)
		node.right = redundantNegations(node.right)
		
		if isinstance(node, ast.Add) and isinstance(node.right, ast.Negate):
			op = node.right.operand
			
			if isinstance(op, ast.Add):
				newRight = redundantNegations(ast.Sub(op.left, op.right))
				return ast.Sub(node.left, newRight)
				
			elif isinstance(op, ast.Sub):
				newRight = redundantNegations(ast.Add(op.left,op.right))
				return ast.Sub(node.left, newRight)
				
			elif isinstance(op, ast.Integer) or isinstance(op, ast.Name) or isinstance(op, ast.FunctionCall):
				return ast.Sub(node.left, op)
				
			else:
				return node
		
		elif isinstance(node, ast.Sub) and isinstance(node.right, ast.Negate):
			return ast.Add(node.left, node.right.operand)
		
		else:
			return node
	
	elif isinstance(node, ast.FunctionCall):
		newArgs = []
		
		for arg in node.args:
			newArgs.append(redundantNegations(arg))
		
		node.args = newArgs
		
		return node
	
	elif isinstance(node, ast.Integer):
		return node
	
	elif isinstance(node, ast.Module):
		newStmts = []
		
		for stmt in node.stmts:
			newStmts.append(redundantNegations(stmt))
		
		node.stmts = newStmts
		return node
	
	elif isinstance(node, ast.Name):
		return node
	
	elif isinstance(node, ast.Negate):
		if isinstance(node.operand, ast.Negate):
			return redundantNegations(node.operand.operand)
		else:
			node.operand = redundantNegations(node.operand)
			return node
	
	elif isinstance(node, ast.UnaryOp):
		node.operand = redundantNegations(node.operand)
		
		return node
