"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		Ouroboros
Date:		2010/09/22
Description:	An analysis that calculates the weight of each symbol.
"""

from lib.ast import *
from lib.util import extractSymbol

args		= []
prereqs	= ['reads', 'spans']
result	= None
sets		= ['weight']

def init():
	from analysis.pass_manager import register
	register('weight', weight, args, prereqs, result, sets)

def weight(node, depth = 0.0):
	if isinstance(node, Assign):
		sym = extractSymbol(node)
		
		sym['weight'] = 1.0 + (10.0 ** depth)
		sym['tmp'] = sym['reads']
	
	elif isinstance(node, Symbol):
		node['weight'] += 1.0 + (10.0 ** depth)
		
		node['tmp'] -= 1
		
		if node['tmp'] == 0:
			node['weight'] = node['weight'] / float(node['span-length'])
	
	for child in node:
		if isinstance(node, BasicBlock):
			weight(child, depth + 1.0)
		
		else:
			weight(child, depth)
