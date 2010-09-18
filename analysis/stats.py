"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/09/018
Description:	Basic statistical anlysis methods.
"""

from lib.ast import *

def countReads(node, count = {}):
	for n in node:
			countReads(n, count)
	
	if isinstance(node, Module):
		return count
	
	elif isinstance(node, Name):
		if count.has_key(node.name):
			count[node.name] += 1
		else:
			count[node.name] = 1

def markReads(node, count):
	for n in node:
		markReads(n, count)
	
	if isinstance(node, Name):
		node['reads'] = count[node.name]
