"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		Ouroboros
Date:		2010/12/06
Description:	Removes variables that are never read from and functions that are
			never called.
"""

from lib.ast import *
from lib.util import classGuard, flatten

analysis	= ['reads']
args		= []

def init():
	from transforms.pass_manager import register
	register('dead_store', eliminateDeadStores, analysis, args)

def eliminateDeadStores(node):
	newChildren = []
	
	for child in node:
		newChildren.append(eliminateDeadStores(child))
	
	#~print("FOO")
	#~print(newChildren)
	
	node.setChildren(flatten(newChildren))
	
	if isinstance(node, Assign) and node.var['reads'] == 0:
		if isinstance(node.exp, FunctionCall):
			return node.exp
		
		elif isinstance(node.exp, Class):
			return node
		
		else:
			return None
	
	elif isinstance(node, Phi) and node.target['reads'] == 0:
		return None
	
	else:
		return node
