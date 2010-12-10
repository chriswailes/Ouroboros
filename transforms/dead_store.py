"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		Ouroboros
Date:		2010/12/06
Description:	Removes variables that are never read from and functions that are
			never called.
"""

from lib.ast import *
from lib.util import classGuard, extractSymbol, flatten

analysis	= ['reads']
args		= []

def init():
	from transforms.pass_manager import register
	register('dead_store', eliminateDeadStores, analysis, args)

def eliminateDeadStores(node):
	newChildren = []
	
	for child in node:
		newChildren.append(eliminateDeadStores(child))
	
	node.setChildren(flatten(newChildren))
	
	if isinstance(node, Assign):
		sym = extractSymbol(node.var)
		
		if sym['reads'] == 0:
			if classGuard(node.exp, Class, FunctionCall):
				return node
			
			else:
				return None
		
		else:
			return node
	
	elif isinstance(node, Phi) and node.target['reads'] == 0:
		return None
	
	else:
		return node
