"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/09/20
Description:	Propigate constants throughout the code.
"""

from lib.ast import *

def init():
	from transforms.pass_manager import register
	register('color', color, analysis, args

def propigateConstants(node, consts = {}):
	
	if isinstance(node, Assign) and isinstance(node.exp, Integer):
		consts[node.var.symbol] = Integer(node.exp.value)
	
	elif isinstance(node, Name) and const.has_key(node.symbol):
		return consts[node.sybmol]
	
	else:
		newChildren = []
		
		for child in node:
			newChildren.append(propigateConstants(child, consts))
		
		node.setChildren(newChildren)
	
	return node
