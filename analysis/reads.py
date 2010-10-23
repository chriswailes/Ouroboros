"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/09/18
Description:	Counts the number of reads each symbol has.
"""

from lib.ast import *
from lib.util import classGuard, extractSymbol

args		= []
prereqs	= []
result	= None

def init():
	from analysis.pass_manager import register
	register('reads', reads, args, prereqs, result)

def reads(node):
	if isinstance(node, Module):
		for sym in node.collectSymbols():
			if sym.has_key('reads'):
				del sym['reads']
	
	if classGuard(node, Assign, Phi) and not extractSymbol(node).has_key('reads'):
		extractSymbol(node)['reads'] = 0
	
	elif classGuard(node, Function):
		for sym in node.argSymbols:
			sym['reads'] = 0
	
	elif isinstance(node, Symbol):
		
		#This is kind of ugly, but because of Python's scoping rules we can
		#read from a variable before it is 'in scope.'
		if node.has_key('reads'):
			#~print("Normal read from {0}".format(node))
			#~print(node['reads'])
			node['reads'] += 1
			#~print(node['reads'])
		else:
			#~print("Messed up Python read from {0}".format(node))
			node['reads'] = 1
			#~print(node['reads'])
	
	#This little hack is here to take care of cases where subscripts are
	#applied to literal values. After the flatten transformation this branch
	#will be taken whenever we see a subscript.
	elif isinstance(node, Subscript) and isinstance(node.symbol, Symbol):
		node.symbol['reads'] += 1
	
	for child in node:
		reads(child)
