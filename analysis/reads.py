"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		Ouroboros
Date:		2010/09/18
Description:	Counts the number of reads each symbol has.
"""

from lib.ast import *
from lib.util import classGuard, extractSymbol

args		= []
prereqs	= []
result	= None
sets		= ['reads']

def init():
	from analysis.pass_manager import register
	register('reads', reads, args, prereqs, result, sets)

def reads(node):
	if classGuard(node, Assign, Phi):
		sym = extractSymbol(node)
		
		if not sym.has_key('reads'):
			sym['reads'] = 0
			
	elif isinstance(node, Function):
		for sym in node.argSymbols:
			sym['reads'] = 0
	
	elif isinstance(node, Symbol):
		#This is kind of ugly, but because of Python's scoping rules we can
		#read from a variable before it is 'in scope.'
		
		if node.has_key('reads'):
			node['reads'] += 1
		else:
			node['reads'] = 1
	
	elif isinstance(node, Subscript) and isinstance(node.symbol, Symbol):
		#This little hack is here to take care of cases where subscripts are
		#applied to literal values. After the flatten transformation this
		#branch will be taken whenever we see a subscript.
		
		node.symbol['reads'] += 1
	
	for child in node:
		reads(child)
