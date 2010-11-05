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
	if isinstance(node, Module):
		alive = []
		for sym in node.collectSymbols():
			if sym.has_key('tmp'):
				del sym['tmp']
	
	if not isinstance(node, Symbol):
		node['pre-alive'] = set(alive)
	
	if isinstance(node, Function):
		for sym in node.argSymbols:
			
			#Functions might have arguments that are never read.
			if sym['reads'] > 0:
				sym['tmp'] = sym['reads']
				alive.append(sym)
	
	for child in node:
		liveness(child, alive)
	
	if classGuard(node, Assign, Phi):
		sym = extractSymbol(node)
		
		if not sym.has_key('tmp'):
			#~print("Sym {0} has {1} reads".format(sym, sym['reads']))
			sym['tmp'] = sym['reads']
			alive.append(sym)
	
	elif isinstance(node, Symbol) or (isinstance(node, Subscript) and isinstance(node.symbol, Symbol)):
		sym = extractSymbol(node)
		
		#~print("Reading {0}".format(sym))
		
		if sym.has_key('tmp'):
			sym['tmp'] -= 1
			
			if sym['tmp'] == 0:
				#~print("Removing {0}".format(sym))
				alive.remove(sym)
			
		else:
			sym['tmp'] = sym['reads']
			alive.append(sym)
	
	if not isinstance(node, Symbol):
		node['post-alive'] = set(alive)
		
		#~ print("Node: {0}".format(node))
		#~ print("Pre-alive: {0}".format(node['pre-alive']))
		#~ print("Post-alive: {0}".format(node['post-alive']))
		#~ print('')
