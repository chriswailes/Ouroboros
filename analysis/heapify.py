"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/09/24
Description:	Locate symbols that need to be heapified.
"""

from lib.ast import *

args		= []
prereqs	= ['scope']
result	= None

def init():
	from analysis.pass_manager import register
	register('heapify', heapify, args, prereqs, result)

def heapify(node):
	if isinstance(node, Module):
		#Mark the default heapify state of all symbols as False.
		for sym in node.collectSymbols():
			sym['heapify'] = False
	
	elif isinstance(node, Function):
		syms  = node.collectSymbols()
		bound = node.collectSymbols('w')
		free  = syms - bound
		
		#Mark any free variables for heapification.
		for sym in free:
			sym['heapify'] = 'data' if sym['scope'] == 'global' else 'closure'
		
		#Mark this function's free variables for later use.
		node['free'] = free
	
	#Run heapify on the node's children.
	for child in node:
		heapify(child)
