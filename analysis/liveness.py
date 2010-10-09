"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/09/18
Description:	Determines the liveness of varaibles at every node in the AST.
"""

from lib.ast import *
from lib.util import classGuard, extractSymbol

args		= []
prereqs	= ['reads']
result	= None

def init():
	from analysis.pass_manager import register
	register('liveness', liveness, args, prereqs, result)

def liveness(node, alive = []):
	node['pre-alive'] = set(alive)
	
	if isinstance(node, Assign):
		sym = extractSymbol(node)
		
		sym['tmp'] = sym['reads']
		alive.append(sym)
	
	elif classGuard(node, Symbol, Subscript):
		sym = extractSymbol(node)
		
		sym['tmp'] -= 1
		
		if sym['tmp'] == 0:
			alive.remove(sym)
	
	elif isinstance(node, Phi):
		sym = node.target
		
		sym['tmp'] = sym['reads']
		alive.append(sym)
	
	for child in node:
		liveness(child, alive)
	
	node['post-alive'] = set(alive)
