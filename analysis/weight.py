"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/09/22
Description:	An analysis that calculates the weight of each symbol.
"""

from lib.ast import *

args		= []
prereqs	= ['reads', 'spans']
result	= None

def init():
	from analysis.pass_manager import register
	register('weight', weight, args, prereqs, result)

def weight(node, depth = 0.0):
	
	if isinstance(node, Assign):
		sym = node.var.symbol
		
		sym['weight'] = 1.0 + (10.0 ** depth)
		sym['tmp'] = sym['reads']
	
	elif isinstance(node, Name):
		sym = node.symbol
		
		sym['weight'] += 1.0 + (10.0 ** depth)
		
		sym['tmp'] -= 1
		
		if sym['tmp'] == 0:
			sym['weight'] = sym['weight'] / float(sym['span'])
	
	for child in node:
		if isinstance(node, BasicBlock):
			weight(child, depth + 1.0)
		
		else:
			weight(child, depth)