"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/09/20
Description:	Propigate constants throughout the code.
"""

from lib.ast import *
from lib.util import classGuard

analysis	= []
args		= []

def init():
	from transforms.pass_manager import register
	register('const_prop', propigateConstants, analysis, args)

def propigateConstants(node, consts = {}):
	#Memorize or replace symbol values, as appropriate.
	if isinstance(node, Assign) and isinstance(node.var, Symbol) and classGuard(node.exp, Boolean, Integer, Name):
		consts[node.var] = node.exp
	
	elif isinstance(node, Symbol) and consts.has_key(node):
		return consts[node]
	
	#Values in Phi nodes should never be replaced.
	if not isinstance(node, Phi):
		newChildren = []
		
		for child in node:
			newChildren.append(propigateConstants(child, consts))
	
		node.setChildren(newChildren)
	
	return node
