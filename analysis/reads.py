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
	for child in node:
		reads(child)
	
	if classGuard(node, Assign, Phi):
		extractSymbol(node)['reads'] = 0
	
	elif isinstance(node, Symbol):
		node['reads'] += 1
	
	#This little hack is here to take care of cases where subscripts are
	#applied to literal values. After the flatten transformation this branch
	#will be taken whenever we see a subscript.
	elif isinstance(node, Subscript) and isinstance(node.symbol, Symbol):
		node.symbol['reads'] += 1
