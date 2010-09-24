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
		sym = node.var.symbol
		sym['tmp'] = sym['reads']
		
		liveness(node.exp, alive)
		
		if sym['tmp'] > 0:
			alive.append(sym)
	
	elif isinstance(node, Name):
		node.symbol['tmp'] -= 1
		
		if node.symbol['tmp'] == 0:
			alive.remove(node.symbol)
	
	else:
		for child in node:
			liveness(child, alive)
	
	node['post-alive'] = set(alive)
