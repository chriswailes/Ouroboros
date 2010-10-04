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
	newChildren = []
	
	for child in node:
		newChildren.append(foldConstants(child))
	
	node.setChildren(newChildren)
	
	if isinstance(node, BinOp):
		#Move constant values to the left when we can.
		if isinstance(node, Add) or isinstance(node, Mul):
			if isinstance(node.right, Integer):
				tmp = node.left
				node.left = node.right
				node.right = tmp
		
		elif isinstance(node, And) or isinstance(node, Or):
			if not isinstance(node.left, Boolean) and isinstance(node.right, Boolean):
				tmp = node.left
				node.left = node.right
				node.right = tmp
		
		#Swap operators if we can.
		if isinstance(node, Add) and isinstance(node.right, Negate):
			node = Sub(node.left, node.right.operand)
		
		elif isinstance(node, Sub) and isinstance(node.right, Negate):
			node = Add(node.left, node.right.operand)
		
		elif isinstance(node, And) or isinstance(node, Or):
			if isinstance(node.left, Not) and isinstance(node.right, Not):
				if isinstance(node, And):
					node = Or(node.left.operand, node.right.operand)
				
				else:
					node = And(node.left.operand, node.right.operand)
		
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
		
		elif isinstance(node.left, Boolean):
			if isinstance(node, And):
				if isinstance(node.left, Tru):
					node = node.right
				
				else:
					node = Fals()
			
			elif isinstance(node, Or):
				if isinstance(node.left, Tru):
					node = Tru()
				
				else:
					node = node.right
	
	elif isinstance(node, Negate):
		op = node.operand
		
		if isinstance(op, Integer):
			value = eval("-{0}".format(op.value))
			node = Integer(value)
		
		elif isinstance(op, Negate):
			node = foldConstants(op.operand)
		
		elif isinstance(op, BinOp):
			cond  = isinstance(op.left, Negate) or isinstance(op.left, Integer)
			cond |= isinstance(op.right, Negate) or isinstance(op.right, Integer)
			
			if cond:
				if isinstance(op, Add):
					newNode = Add(Negate(op.left), Negate(op.right))
					node = foldConstants(newNode)
				
				elif isinstance(op, Sub):
					newNode = Sub(Negate(op.left), Negate(op.right))
					node = foldConstants(newNode)
	
	elif isinstance(node, Not):
		op = node.operand
		
		if isinstance(op, Tru):
			node = Fals()
		
		elif isinstance(op, Fals):
			node = Tru()
		
		elif isinstance(op, BinOp):
			cond  = isinstance(op.left, Not) or isinstance(op.left, Boolean)
			cond |= isinstance(op.right, Not) or isinstance(op.right, Boolean)
			
			if cond:
				if isinstance(op, And):
					newNode = Or(Not(op.left), Not(op.right))
					node = foldConstants(newNode)
				
				elif isinstance(op, Or):
					newNode = And(Not(op.left), Not(op.right))
					node = foldConstants(newNode)
	
	return node
