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
	
	else:
		if isinstance(node, Function):
			syms  = node.collectSymbols()
			bound = collectAssigned(node, [])
			free  = syms - bound
			
			#Here we mark any new symbols as either 'global' or 'local'.  Global
			#symbols are defined in the main function and can be put in the data
			#section.  Local variables that apear as free variables in lambda
			#definitions need to be packed into a closure.
			for sym in bound:
				if node.name.name == 'main':
					sym['scope'] = 'global'
				
				else:
					sym['scope'] = 'local'
			
			#Mark any free variables for heapification.
			for sym in free:
				sym['heapify'] = 'data' if sym['scope'] == 'global' else 'closure'
			
			#Mark this function's free variables for later use.
			node['free'] = free
			
			print("Symbols for function {0}: {1}".format(node.name, syms))
			print("Bound symbols: {0}".format(bound))
			print("Free symbols: {0}".format(free))
			
			print("Free symbol scope:")
			for sym in free:
				print("\t{0} : {1}".format(sym, sym['scope']))
			
			print('')
	
		for child in node:
			heapify(child)


def collectAssigned(node, assigned = []):
	if isinstance(node, Function):
		#~print("Collecting assignments for {0}".format(node.name))
		#~print("Bound so far: {0}".format(assigned))
		assigned.extend(list(node.argSymbols))
	
	elif isinstance(node, Assign):
		assigned.append(extractSymbol(node.var))
		
		#~print("In assign from {0}".format(extractSymbol(node.var)))
	
	elif isinstance(node, Phi):
		assigned.append(node.target)
	
	for child in node:
		collectAssigned(child, assigned)
	
	return set(assigned)
