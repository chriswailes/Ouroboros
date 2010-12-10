"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		Ouroboros
Date:		2010/09/24
Description:	Locate symbols that need to be heapified.
"""

from lib.ast import *

args		= []
prereqs	= ['scope']
result	= None
sets		= ['heapify']

def init():
	from analysis.pass_manager import register
	register('heapify', heapify, args, prereqs, result, sets)

def heapify(node):
	if isinstance(node, Function):
		syms  = node.collectSymbols()
		bound = node.collectSymbols('w')
		
		for sym in syms:
			if sym in bound:
				sym['heapify'] = False
			
			elif sym['scope'] == 'global':
				sym['heapify'] = 'data'
			
			else:
				sym['heapify'] = 'closure'
		
		#Mark this function's free variables for later use.
		node['free'] = syms - bound
	
	#Run heapify on the node's children.
	for child in node:
		heapify(child)
