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
	newChildren	= []
	newInPlace	= False
	preStmts		= []
	ret			= node
	
	if isinstance(node, Assign):
		newInPlace = True
	
	elif isinstance(node, BasicBlock):
		st = node.st
		newInPlace = True
	
	for child in node:
		childPreStmts, newChild = flatten(child, st, newInPlace)
		
		if isinstance(node, BasicBlock):
			newChildren.append(childPreStmts)
			newChildren.append(newChild)
		
		else:
			preStmts.append(childPreStmts)
			newChildren.append(newChild)
	
	#Flatten our collections.
	newChildren = util.flatten(newChildren)
	preStmts = util.flatten(preStmts)
	
	#Set our children.
	node.setChildren(newChildren)
	
	if (isinstance(node, UnaryOp) or isinstance(node, BinOp) or isinstance(node, FunctionCall)) and not inplace:
		ret = Name(st.getSymbol(assign = True))
		preStmts.append(Assign(ret, node))
	
	if isinstance(node, Module):
		return ret
	
	else:
		return preStmts, ret
