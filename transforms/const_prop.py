"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/09/20
Description:	Propigate constants throughout the code.
"""

from lib.ast import *

def propigateConstants(tree):
	consts = collectConsts(tree)
	tree = replaceConsts(tree, consts)
	
	return tree
	

def collectConsts(node):
	consts = {}
	
	#~ print node.__class__.__name__
	
	for child in node:
		consts.update(collectConsts(child))
	
	if isinstance(node, Assign) and isinstance(node.exp, Integer):
		consts[node.var.symbol] = node.exp.value
	
	return consts

def replaceConsts(node, consts):
	newChildren = []
	
	for child in node:
		newChildren.append(replaceConsts(child, consts))
	
	node.setChildren(newChildren)
	
	if isinstance(node, Name) and consts.has_key(node.symbol):
		return Integer(consts[node.symbol])
	else:
		return node
