"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/09/24
Description:	Locate symbols that need to be heapified.
"""

from lib.ast import *
from lib.util import extractSymbol

args		= []
prereqs	= []
result	= None

def init():
	from analysis.pass_manager import register
	register('heapify', heapify, args, prereqs, result)

def heapify(node):
	if isinstance(node, Module):
		
		#Mark the default heapify state of all symbols as False.
		for sym in node.collectSymbols():
			sym['heapify'] = False
		
		#Run heapify on each of this module's functions.
		for fun in node.functions:
			heapify(fun)
	
	elif isinstance(node, Function):
		syms  = node.collectSymbols()
		bound = collectAssigned(node)
		free  = syms - bound
		
		for sym in syms:
			if sym in free:
				sym['heapify'] = True
		
		#~print("Symbols for function {0}: {1}".format(node.name, syms))
		#~print("Bound symbols: {0}".format(bound))
		#~print("Free symbols: {0}".format(free))
		#~print('')


def collectAssigned(node, assigned = []):
	
	for child in node:
		collectAssigned(child, assigned)
	
	if isinstance(node, Function):
		assigned += list(node.argSymbols)
		
		return set(assigned)
	
	elif isinstance(node, Assign):
		assigned.append(extractSymbol(node.var))
	
	elif isinstance(node, Phi):
		assigned.append(node.target)
