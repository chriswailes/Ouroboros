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
	if isinstance(node, Module):
		print(node)
	
	node['pre-alive'] = set(alive)
	
	if isinstance(node, Assign):
		print("In assignment for symbol {0}".format(node.var.symbol))
		
		if isinstance(node.var, Name):
			sym = node.var.symbol
		else:
			sym = node.var.name.symbol
		
		print("Symbol {0} has {1} reads".format(sym, sym['reads']))
		sym['tmp'] = sym['reads']
		alive.append(sym)
	
	elif isinstance(node, Name):
		print("In read of symbol {0}".format(node.symbol))
		node.symbol['tmp'] -= 1
		
		if node.symbol['tmp'] == 0:
			print("Removing {0} from the live set".format(node.symbol))
			alive.remove(node.symbol)
	
	elif isinstance(node, Subscript):
		print("In read of subscripted symbol {0}".format(node.name.symbol))
		node.name.symbol['tmp'] -= 1
		
		if node.name.symbol['tmp'] == 0:
			print("Removing {0} from the live set".format(node.name.symbol))
			alive.remove(node.name.symbol)
	
	elif isinstance(node, Phi):
		sym = node.target.symbol
		sym['tmp'] = sym['reads']
		alive.append(sym)
	
	for child in node:
		liveness(child, alive)
	
	node['post-alive'] = set(alive)
