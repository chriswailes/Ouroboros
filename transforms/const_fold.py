"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/09/01
Description:	A transformation that folds constants.
"""

from lib import ast

def foldConstants(node):
	if isinstance(node, ast.Assign):
		node.exp = foldConstants(node.exp)
		
		return node
	
	elif isinstance(node, ast.BinOp):
		#Fold the left and right operands.
		node.left = foldConstants(node.left)
		node.right = foldConstants(node.right)
		
		#Move constant values to the left when we can.
		if isinstance(node, ast.Add) or isinstance(node, ast.Mul):
			if isinstance(node.right, ast.Integer):
				tmp = node.left
				node.left = node.right
				node.right = tmp
		
		if isinstance(node.left, ast.Integer):
			#If they are both Integers, calculate their value.
			if isinstance(node.right, ast.Integer):
				value = eval("{0} {1} {2}".format(node.left.value, node.operator, node.right.value))
				return ast.Integer(value)
			
			#If they aren't both integers we might be able to lift an integer from the right side.
			elif isinstance(node.right, ast.BinOp) and isinstance(node.right.left, ast.Integer):
				foldOK = isinstance(node, ast.Add) and (isinstance(node, ast.Add) or isinstance(node, ast.Sub))
				foldOK = foldOK or isinstance(node, ast.Sub) and (isinstance(node, ast.Add) or isinstance(node, ast.Sub))
				foldOK = foldOK or (isinstance(node, ast.Mul) and isinstance(node.right, ast.Mul))
				
				if foldOK:
					value = eval("{0} {1} {2}".format(node.left.value, node.operator, node.right.left.value))
					
					node.right.left = ast.Integer(value)
					return node.right
		
		return node
	
	elif isinstance(node, ast.FunctionCall):
		newArgs = []
		
		for arg in node.args:
			newArgs.append(foldConstants(arg))
		
		node.args = newArgs
		
		return node
	
	elif isinstance(node, ast.Integer):
		return node
	
	elif isinstance(node, ast.Module):
		newStmts = []
		
		for stmt in node.stmts:
			newStmts.append(foldConstants(stmt))
		
		node.stmts = newStmts
		
		return node
	
	elif isinstance(node, ast.Name):
		return node
	
	elif isinstance(node, ast.UnaryOp):
		node.operand = foldConstants(node.operand)
		
		if isinstance(node.operand, ast.Integer):
			value = eval("{0} {1}".format(node.operator, node.operand.value))
			return ast.Integer(value)
		
		return node
