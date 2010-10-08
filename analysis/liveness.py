"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/09/18
Description:	Determines the liveness of varaibles at every node in the AST.
"""

from lib.ast import *

args		= []
prereqs	= ['reads']
result	= None

def init():
	from analysis.pass_manager import register
	register('liveness', liveness, args, prereqs, result)

def liveness(node, alive = []):
	node['pre-alive'] = set(alive)
	
	if isinstance(node, Assign):
		if isinstance(node.var, Name):
			sym = node.var.symbol
		else:
			sym = node.var.name.symbol
		
		sym['tmp'] = sym['reads']
		alive.append(sym)
	
	elif isinstance(node, Name):
		node.symbol['tmp'] -= 1
		
		if node.symbol['tmp'] == 0:
			alive.remove(node.symbol)
	
	elif isinstance(node, Subscript):
		node.name.symbol['tmp'] -= 1
		
		if node.name.symbol['tmp'] == 0:
			alive.remove(node.name.symbol)
	
	elif isinstance(node, Phi):
		sym = node.target.symbol
		sym['tmp'] = sym['reads']
		alive.append(sym)
	
	for child in node:
		liveness(child, alive)
	
	node['post-alive'] = set(alive)
