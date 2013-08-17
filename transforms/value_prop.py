"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		Ouroboros
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
	# This will only propigate local constants.
	consts = propagateValuesPrime(tree, {})
	
	# Here we sort out the global constants.
	globls = {}
	for const in consts:
		if const['scope'] == 'global':
			globls[const] = consts[const]
	
	# This pass will replace global constant values.  This is what propigates
	# function names.  More work will need to go into this for proper scoping
	# (if Python can be said to have proper scoping).
	propagateValuesPrime(tree, globls, False)

def propagateValuesPrime(node, consts, gather = True):
	# Memorize or replace symbol values, as appropriate.
	if gather:
		if isinstance(node, Assign) and isinstance(node.var, Symbol) and classGuard(node.exp, Boolean, Integer, Name, Symbol):
			consts[node.var] = node.exp
		
		elif isinstance(node, Phi) and len(node.srcs) == 1 and consts.has_key(node.srcs[0]):
			consts[node.target] = consts[node.srcs[0]]
	
	elif isinstance(node, Symbol) and consts.has_key(node):
		return consts[node]
	
	# Values in Phi nodes should never be replaced.
	if isinstance(node, While):
		# This looks all weird because we have to change the order of the
		# While node's children to propigate values appropriately.
		
		children = node.getChildren()
		children = children[1:] + children[0:1]
		
		newChildren = [propagateValuesPrime(child, consts, gather) for child in children]
		
		newChildren = newChildren[-1:] + newChildren[0:-1]
		
		node.setChildren(newChildren)
	
	elif not isinstance(node, Phi):
		newChildren = [propagateValuesPrime(child, consts, gather) for child in node]
		node.setChildren(newChildren)
	
	return consts if isinstance(node, Module) else node
