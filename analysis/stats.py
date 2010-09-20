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
		if node.var.symbol in node['post-alive']:
			alive[node.var.symbol] = count
	
	for child in node:
		inc += calculateSpans(child)
	
	count += inc
	
	for sym in alive:
		if not sym in node['post-alive']:
			sym['span'] = count - alive[sym]
			del alive[sym]
	
	return inc
