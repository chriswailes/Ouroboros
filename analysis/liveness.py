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
	
	if not isinstance(node, Symbol):
		node['pre-alive'] = set(alive)
	
	for child in node:
		liveness(child, alive)
	
	if classGuard(node, Assign, Phi):
		sym = extractSymbol(node)
		
		#~print("In assignment for {0}".format(sym))
		#~print("Live set: {0}".format(alive))
		
		sym['tmp'] = sym['reads']
		alive.append(sym)
	
	elif classGuard(node, Symbol, Subscript):
		sym = extractSymbol(node)
		
		#~print("In read of {0}".format(sym))
		
		sym['tmp'] -= 1
		
		if sym['tmp'] == 0:
			#~print("Removing {0} from the live set".format(sym))
			alive.remove(sym)
	
	if not isinstance(node, Symbol):
		node['post-alive'] = set(alive)
