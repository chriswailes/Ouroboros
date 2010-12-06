"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		Ouroboros
Date:		2010/09/01
Description:	A transformation that folds constants.
"""

from lib.ast import *
from lib.util import reType

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
		
		####################
		# Literal Rotation #
		####################
		
		#Move constant values to the left when we can.
		if classGuard(node, Add, Mul) and classGuard(node.right, Integer, Boolean):
			tmp = node.left
			node.left = node.right
			node.right = tmp
		
		######################
		# Operator Reduction #
		######################
		
		#Swap operators if we can.
		if isinstance(node, Add) and isinstance(node.right, Negate):
			node = Sub(node.left, node.right.operand)
		
		elif isinstance(node, Sub) and isinstance(node.right, Negate):
			node = Add(node.left, node.right.operand)
		
		elif isinstance(node, And) or isinstance(node, Or):
			
			#The only place it makes sense to use De Morgan's law is if both
			#the operands are Not nodes.  Otherwise we would be replacing one
			#Not node with two.
			if isinstance(node.left, Not) and isinstance(node.right, Not):
				if isinstance(node, And):
					node = Or(node.left.operand, node.right.operand)
				
				else:
					node = And(node.left.operand, node.right.operand)
		
		###################
		# Literal Lifting #
		###################
		
		#Try to lift literal values out of the right hand side.
		if isinstance(node.right, BinOp) and isinstance(node.right.left, Literal):
			#There are only several combinations of operations that
			#we can do this for so we must check to see if this is
			#one of those cases.
			
			cond  = isinstance(node, Add) and classGuard(node.right, Add, Sub)
			cond |= isinstance(node, Sub) and classGuard(node.right, Add, Sub)
			cond |= isinstance(node, Mul) and isinstance(node.right, Mul)
			cond |= isinstance(node, And) and isinstance(node.right, And)
			cond |= isinstance(node, Or)  and isinstance(node.right, Or)
			
			if cond:
				#If we are are currently at a Sub node we need to
				#swap our operator.
				if isinstance(node, Sub):
					node.right = (Sub if isinstance(node.right, Add) else Add)(node.right.left, node.right.right)
				
				#Left Rotate
				node.right.left = node.__class__(node.left, node.right.left)
				node = node.right
		
		########################
		# Constant Calculation #
		########################
		
		#Calcluate constant values if possible.
		if isinstance(node.left, Literal):
			#Boolean simplification only relies on the left value.  Try that first.
			if isinstance(node, And):
				if node.left.value:
					node = node.right
				
				else:
					node = node.left
			
			elif isinstance(node, Or):
				if node.left.value:
					node = node.left
				
				else:
					node = node.right
			
			#For all other operating types we need two Literals.
			elif isinstance(node.right, Literal):
				value = eval("{0} {1} {2}".format(node.left.value, node.operator, node.right.value))
				
				node = reType(value)
	
	elif isinstance(node, UnaryOp):
		nodeKlass = node.__class__
		opKlass = node.operand.__class__
		
		if isinstance(node.operand, Literal):
			value = eval("{0}{1}".format(node.operator, node.operand.value))
			node = reType(value)
		
		elif isinstance(node.operand, nodeKlass):
			#If the operand is the same class as the current node then we can
			#remove the redundant operations.
			node = node.operand.operand
		
		elif isinstance(node.operand, BinOp):
			cond  = classGuard(node.operand.left, nodeKlass, Literal)
			cond |= classGuard(node.operand.right, nodeKlass, Literal)
			
			if cond:
				newNode = opKlass(nodeKlass(node.operand.left), nodeKlass(node.operand.right))
				node = foldConstants(newNode)
	
	return node
