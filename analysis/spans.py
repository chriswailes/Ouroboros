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
	startCount = count

	#We don't want to count the nodes that are children of lists and
	#dictionaries as this would distort the wieght of variables that span them.
	if not isinstance(node, Value):
		for child in node:
			subInc = spans(child, count)
			inc   += subInc
			count += subInc
	
	if isinstance(node, Assign) or isinstance(node, Phi):
		#Due to SSA form we know this variable isn't already alive.
		sym = extractSymbol(node)
		
		sym['spans-funcall'] = False
		
		if sym in node['post-alive']:
			alive[sym] = startCount
		else:
			sym['span-start'] = sym['span-end'] = startCount
			sym['span'] = 0
	
	elif isinstance(node, FunctionCall):
		for sym in node['pre-alive']:
			if sym in node['post-alive']:
				sym['spans-funcall'] = True
	
	deletes = []
	
	for sym in alive:
		if not sym in node['post-alive']:
			sym['span-start'] = alive[sym]
			sym['span-end'  ] = count
			sym['span'] = count - alive[sym]
			deletes.append(sym)
	
	for sym in deletes:
		del alive[sym]
		
	return inc
