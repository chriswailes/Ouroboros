"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/09/20
Description:	Propigate values throughout the code.
"""

from lib.ast import *
from lib.util import classGuard

analysis	= ['scope']
args		= []

def init():
	from transforms.pass_manager import register
	register('value_prop', propagateValues, analysis, args)

def propagateValues(tree):
	#This will only propigate local constants.
	consts = propagateValuesPrime(tree, {})
	
	#Here we sort out the global constants.
	globls = {}
	for const in consts:
		if const['scope'] == 'global':
			globls[const] = consts[const]
	
	#This pass will replace global constant values.  This is what propigates
	#function names.  More work will need to go into this for proper scoping
	#(if Python can be said to have proper scoping).
	propagateValuesPrime(tree, globls, False)

def propagateValuesPrime(node, consts, gather = True):
	#Memorize or replace symbol values, as appropriate.
	if gather and isinstance(node, Assign) and isinstance(node.var, Symbol) and classGuard(node.exp, Boolean, Integer, Name, Symbol):
		consts[node.var] = node.exp
	
	elif isinstance(node, Symbol) and consts.has_key(node):
		return consts[node]
	
	#Values in Phi nodes should never be replaced.
	if not isinstance(node, Phi):
		newChildren = [propagateValuesPrime(child, consts, gather) for child in node]
		node.setChildren(newChildren)
	
	return consts if isinstance(node, Module) else node
