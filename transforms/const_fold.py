"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/09/01
Description:	A transformation that folds constants.
"""

from lib.ast import *

analysis	= []
args		= []

def init():
	from transforms.pass_manager import register
	register('const_fold', foldConstants, analysis, args)

def foldConstants(node):
	if isinstance(node, Assign):
		node.exp = foldConstants(node.exp)
		
		return node
	
	elif isinstance(node, BasicBlock):
		newChildren = []
		
		for child in node:
			newChildren.append(foldConstants(child))
		
		node.children = newChildren
		return node
	
	elif isinstance(node, BinOp):
		#Fold the left and right operands.
		node.left = foldConstants(node.left)
		node.right = foldConstants(node.right)
		
		#Move constant values to the left when we can.
		if isinstance(node, Add) or isinstance(node, Mul):
			if isinstance(node.right, Integer):
				tmp = node.left
				node.left = node.right
				node.right = tmp
		
		#Swap operators if our right hand value is a negation.
		if isinstance(node, Add) and isinstance(node.right, Negate):
			node = Sub(node.left, node.right.operand)
		
		elif isinstance(node, Sub) and isinstance(node.right, Negate):
			node = Add(node.left, node.right.operand)	
		
		#Calcluate constant values.
		if isinstance(node.left, Integer):
			#If they are both Integers, calculate their value.
			if isinstance(node.right, Integer):
				value = eval("{0} {1} {2}".format(node.left.value, node.operator, node.right.value))
				return Integer(value)
			
			#If they aren't both integers we might be able to lift an integer from the right side.
			elif isinstance(node.right, BinOp) and isinstance(node.right.left, Integer):
				value = eval("{0} {1} {2}".format(node.left.value, node.operator, node.right.left.value))
				
				cond  = isinstance(node, Add) and (isinstance(node.right, Add) or isinstance(node.right, Sub))
				cond |= isinstance(node, Mul) and isinstance(node.right, Mul)
				
				if cond:
					node.right.left = Integer(value)
					node = node.right
				
				elif isinstance(node, Sub):
					if isinstance(node.right, Add):
						node = Sub(Integer(value), node.right.right)
					
					elif isinstance(node.right, Sub):
						node = Add(Integer(value), node.right.right)
		
		return node
	
	elif isinstance(node, FunctionCall):
		newArgs = []
		
		for arg in node.args:
			newArgs.append(foldConstants(arg))
		
		node.args = newArgs
		
		return node
	
	elif isinstance(node, If):
		node.cond = foldConstants(node.cond)
		node.then = foldConstants(node.then)
		node.els  = foldConstants(node.els )
		
		return node
	
	elif isinstance(node, Integer):
		return node
	
	elif isinstance(node, Module):
		node.block = foldConstants(node.block)
		
		return node
	
	elif isinstance(node, Name):
		return node
	
	elif isinstance(node, Negate):
		node.operand = foldConstants(node.operand)
		
		if isinstance(node.operand, Add):
			op = node.operand
			if isinstance(op.left, Negate) or isinstance(op.right, Negate):
				newNode = Add(Negate(op.left), Negate(op.right))
				return foldConstants(newNode)
			
			else:
				return node
		
		elif isinstance(node.operand, Integer):
			value = eval("-{0}".format(node.operand.value))
			return Integer(value)
		
		elif isinstance(node.operand, Negate):
			return foldConstants(node.operand.operand)
		
		elif isinstance(node.operand, Sub):
			op = node.operand
			
			cond  = isinstance(op.left, Negate) or isinstance(op.left, Integer)
			cond |= isinstance(op.right, Negate) or isinstance(op.right, Integer)
			
			if cond:
				newNode = Sub(Negate(op.left), Negate(op.right))
				return foldConstants(newNode)
			
			else:
				return node
		
		else:
			return node
