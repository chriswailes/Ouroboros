"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/09/18
Description:	Counts the span of each symbol.
"""

from lib.ast import *
from lib.util import extractSymbol

args		= []
prereqs	= ['liveness']
result	= None
sets		= ['spans-funcall', 'span-start', 'span-end', 'span']

def init():
	from analysis.pass_manager import register
	register('spans', spans, args, prereqs, result, sets)

def spans(node, count = 0, alive = None):
	inc = 1
	
	if isinstance(node, Module):
		alive = {}
	
	#Count the spans over our children.
	for child in node:
		subInc = spans(child, count, alive)
		inc   += subInc
		count += subInc
	
	if classGuard(node, Assign, Phi):
		#Due to SSA form we know this variable isn't already alive.
		sym = extractSymbol(node)
		
		sym['spans-funcall'] = False
		
		if sym in node['post-alive']:
			alive[sym] = count
		else:
			sym['span-start'] = sym['span-end'] = count
			sym['span'] = 0
	
	elif isinstance(node, Function):
		for sym in node.argSymbols:
			sym['spans-funcall'] = False
			
			if sym in node['post-alive']:
				alive[sym] = count
			else:
				sym['span-start'] = sym['span-end'] = count
				sym['span'] = 0
	
	elif isinstance(node, FunctionCall):
		#Mark functions that span this function call.
		for sym in node['pre-alive']:
			if sym in node['post-alive']:
				sym['spans-funcall'] = True
	
	#This is here so we don't change the alive list while we are iterating
	#through it.
	deletes = []
	
	#Symbols don't have any pre/post-alive information due to their Singleton
	#nature.
	if not classGuard(node, Name, String, Symbol):
		for sym in alive:
			if isinstance(node, Function) or sym not in node['post-alive']:
				sym['span-start'] = alive[sym]
				sym['span-end'  ] = count - 1
				sym['span'] = sym['span-end'] - sym['span-start']
				
				deletes.append(sym)
	
	for sym in deletes:
		del alive[sym]
	
	return inc
