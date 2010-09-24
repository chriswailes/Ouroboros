"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/09/20
Description:	Propigate constants throughout the code.
"""

from lib.ast import *

analysis	= []
args		= []

def init():
	from transforms.pass_manager import register
	register('const_prop', propigateConstants, analysis, args)

def propigateConstants(node, consts = {}):
	if isinstance(node, Assign) and isinstance(node.exp, Integer):
		consts[node.var.symbol] = Integer(node.exp.value)
	
	elif isinstance(node, Name) and consts.has_key(node.symbol):
		return consts[node.symbol]
	
	else:
		newChildren = []
		
		for child in node:
			newChildren.append(propigateConstants(child, consts))
		
		node.setChildren(newChildren)
	
	return node
