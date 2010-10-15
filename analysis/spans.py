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

def init():
	from analysis.pass_manager import register
	register('spans', spans, args, prereqs, result)

def spans(node, count = 0, alive = {}):
	inc = 1
	
	#Count the spans over our children.
	for child in node:
		subInc = spans(child, count)
		inc   += subInc
		count += subInc
	
	if classGuard(node, Assign, Phi):
		#Due to SSA form we know this variable isn't already alive.
		sym = extractSymbol(node)
		
		sym['spans-funcall'] = False
		
		if sym in node['post-alive']:
			alive[sym] = count
		else:
			sym['span-start'] = sym['span-end'] = startCount
			sym['span'] = 0
	
	elif isinstance(node, FunctionCall):
		for sym in node['pre-alive']:
			if sym in node['post-alive']:
				sym['spans-funcall'] = True
	
	#This is here so we don't change the alive list while we are iterating
	#through it.
	deletes = []
	
	#Symbols don't have any pre/post-alive information due to their Singleton
	#nature.
	if not isinstance(node, Symbol):
		if isinstance(node, Assign):
			print("In {0}".format(node))
			print("Pre-alive: {0}".format(node['pre-alive']))
			print("Post-alive: {0}".format(node['post-alive']))
			print("Alive: {0}".format(alive))
			print('')
		
		for sym in alive:
			if not sym in node['post-alive']:
				print("Marking symbol {0}".format(sym))
				sym['span-start'] = alive[sym]
				sym['span-end'  ] = count - 1
				sym['span'] = sym['span-end'] - sym['span-start']
				
				print("Start: {0} End: {1}\n".format(alive[sym], count))
				deletes.append(sym)
	
	for sym in deletes:
		del alive[sym]
		
	return inc
