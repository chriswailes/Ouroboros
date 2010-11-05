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
		print("Running heapify on {0}\n".format(node))
		
		print(node.toPython())
		
		#Mark the default heapify state of all symbols as False.
		for sym in node.collectSymbols():
			sym['heapify'] = False
		
		#Run heapify on each of this module's functions.
		for fun in node.functions:
			heapify(fun)
	
	else:
		if isinstance(node, Function):
			syms  = node.collectSymbols()
			bound = node.collectSymbols('w')
			free  = syms - bound
			
			print("Heapify for function {0}".format(node.name.name))
			print("Used symbols {0}".format(syms))
			print("Bound: {0}\n".format(bound))
			
			#Here we mark any new symbols as either 'global' or 'local'.  Global
			#symbols are defined in the main function and can be put in the data
			#section.  Local variables that apear as free variables in lambda
			#definitions need to be packed into a closure.
			for sym in bound:
				print("Assigning scope to {0}".format(sym))
				if node.name.name == 'main':
					sym['scope'] = 'global'
				
				else:
					sym['scope'] = 'local'
			
			#Mark any free variables for heapification.
			for sym in free:
				print("Sym: {0}".format(sym))
				sym['heapify'] = 'data' if sym['scope'] == 'global' else 'closure'
			
			#Mark this function's free variables for later use.
			node['free'] = free
			
			#~print("Symbols for function {0}: {1}".format(node.name, syms))
			#~print("Bound symbols: {0}".format(bound))
			#~print("Free symbols: {0}".format(free))
			#~
			#~print("Free symbol scope:")
			#~for sym in free:
				#~print("\t{0} : {1}".format(sym, sym['scope']))
			#~
			#~print('')
	
		for child in node:
			heapify(child)
