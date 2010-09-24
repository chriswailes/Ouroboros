"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/09/01
Description:	A transformation that flattens the provided AST.
"""

from lib.ast import *
from lib import util

analysis	= []
args		= []

def init():
	from transforms.pass_manager import register
	register('flatten', flatten, analysis, args)

def flatten(node, st = None, inplace = False):
	if isinstance(node, Assign):
		preStmts, node.exp = flatten(node.exp, st, True)
		
		return preStmts, node
	
	elif isinstance(node, BasicBlock):
		newChildren = []
		
		for child in node:
			preChildren, newChild = flatten(child, node.st, True)
			
			newChildren.append(preChildren)
			newChildren.append(newChild)
		
		node.children = util.flatten(newChildren)
		
		return [], node
	
	elif isinstance(node, BinOp):
		leftPreStmts, node.left = flatten(node.left, st)
		rightPreStmts, node.right = flatten(node.right, st)
		
		preStmts = util.flatten([leftPreStmts, rightPreStmts])
		
		if inplace:
			return preStmts, node
		else:
			var = Name(st.getSymbol(assign = True))
			preStmts.append(Assign(var, node))
			return preStmts, var
	
	elif isinstance(node, FunctionCall):
		preStmts = []
		newArgs = []
		
		for arg in node.args:
			tmpPreStmts, newArg = flatten(arg, st)
			
			preStmts.append(tmpPreStmts)
			newArgs.append(newArg)
		
		preStmts = util.flatten(preStmts)
		node.args = newArgs
		
		if inplace:
			return preStmts, node
		else:
			var = Name(st.getSymbol(assign = True))
			preStmts.append(Assign(var, node))
			return preStmts, var
	
	elif isinstance(node, If):
		preNodes, node.cond = flatten(node.cond, st)
		
		#These two nodes are BasicBlocks and will supply their own VFiles
		discard, node.then = flatten(node.then)
		discard, node.els = flatten(node.els)
		
		return preNodes, node
	
	elif isinstance(node, Integer):
		return [], node
	
	elif isinstance(node, Module):
		#The BasicBlock will have its own VFile.
		discard, node.block = flatten(node.block)
		
		return node
	
	elif isinstance(node, Name):
		return [], node
	
	elif isinstance(node, UnaryOp):
		preStmts, node.operand = flatten(node.operand, st)
		
		if inplace:
			return util.flatten(preStmts), node
		else:
			var = Name(st.getSymbol(assign = True))
			preStmts.append(Assign(var, node))
			return util.flatten(preStmts), var

