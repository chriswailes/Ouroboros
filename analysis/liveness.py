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
	
	if classGuard(node, Assign, Phi):
		sym = extractSymbol(node)
		
		sym['tmp'] = sym['reads']
		alive.append(sym)
	
	elif classGuard(node, Function, Lambda):
		for sym in node.argSymbols:
			
			#Functions might have arguments that are never read.
			if sym['reads'] > 0:
				sym['tmp'] = sym['reads']
				alive.append(sym)				
	
	elif classGuard(node, Symbol, Subscript):
		sym = extractSymbol(node)
		
		sym['tmp'] -= 1
		
		if sym['tmp'] == 0:
			alive.remove(sym)
	
	for child in node:
		liveness(child, alive)
	
	if not isinstance(node, Symbol):
		node['post-alive'] = set(alive)
