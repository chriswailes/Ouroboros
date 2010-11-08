"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/09/20
Description:	Propigate constants throughout the code.
"""

from lib.ast import *
from lib.util import classGuard

analysis	= ['scope']
args		= []

def init():
	from transforms.pass_manager import register
	register('const_prop', propigateConstants, analysis, args)

def propigateConstants(tree):
	
	#This will only propigate local constants.
	consts = propigateConstantsPrime(tree, {})
	
	#Here we sort out the global constants.
	globls = {}
	for const in consts:
		if const['scope'] == 'global':
			globls[const] = consts[const]
	
	#This pass will replace global constant values.  This is what propigates
	#function names.  More work will need to go into this for proper scoping
	#(if Python can be said to have proper scoping).
	propigateConstantsPrime(tree, globls, False)

def propigateConstantsPrime(node, consts, gather = True):
	#Memorize or replace symbol values, as appropriate.
	if gather and isinstance(node, Assign) and isinstance(node.var, Symbol) and classGuard(node.exp, Boolean, Integer, Name):
		consts[node.var] = node.exp
	
	elif isinstance(node, Symbol) and consts.has_key(node):
		return consts[node]
	
	#Values in Phi nodes should never be replaced.
	if not isinstance(node, Phi):
		newChildren = [propigateConstantsPrime(child, consts, gather) for child in node]
		node.setChildren(newChildren)
	
	return consts if isinstance(node, Module) else node
