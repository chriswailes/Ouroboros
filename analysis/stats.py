"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/09/018
Description:	Basic statistical anlysis methods.
"""

from lib.ast import *

def countReads(node):
	for child in node:
		countReads(child)
	
	if isinstance(node, Assign):
		node.var.symbol['reads'] = 0
	
	elif isinstance(node, Name):
		node.symbol['reads'] += 1

def calculateSpans(node, count = 0, alive = {}):
	inc = 1
	
	if isinstance(node, Assign):
		#Due to SSA form we know this variable isn't already alive.
		
		sym = node.var.symbol
		
		if sym in node['post-alive']:
			alive[sym] = count
		else:
			sym['span-start'] = sym['span-end'] = count
			sym['span'] = 0
	
	for child in node:
		subInc = calculateSpans(child, count)
		inc   += subInc
		count += subInc
	
	deletes = []
	
	for sym in alive:
		if (not sym in node['post-alive']) or isinstance(node, Module):
			sym['span-start'] = alive[sym]
			sym['span-end'  ] = count
			sym['span'] = count - alive[sym]
			deletes.append(sym)
	
	for sym in deletes:
		del alive[sym]
	
	#~if isinstance(node, Module):
		#~for sym in alive:
			#~sym['span-start'] = alive[sym]
			#~sym['span-end'  ] = count
			#~sym['span'] = count - alive[sym]
		
	return inc
