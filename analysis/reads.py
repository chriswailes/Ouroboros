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
	if classGuard(node, Assign, Phi):
		extractSymbol(node)['reads'] = 0
	
	elif classGuard(node, Function, Lambda):
		for sym in node.argSymbols:
			sym['reads'] = 0
	
	elif isinstance(node, FunctionCall) and isinstance(node.name, Symbol):
		
		if node.name.has_key('reads'):
			node.name['reads'] += 1
		
		else:
			node.name['reads'] = 1
	
	elif isinstance(node, Symbol):
		
		if node.has_key('reads'):
			node['reads'] += 1
		
		else:
			node['reads'] = 1
	
	#This little hack is here to take care of cases where subscripts are
	#applied to literal values. After the flatten transformation this branch
	#will be taken whenever we see a subscript.
	elif isinstance(node, Subscript) and isinstance(node.symbol, Symbol):
		node.symbol['reads'] += 1
	
	for child in node:
		reads(child)
