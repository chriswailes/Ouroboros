"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/09/18
Description:	Counts the number of reads each symbol has.
"""

from lib.ast import *

args		= []
prereqs	= []
result	= None

def init():
	from analysis.pass_manager import register
	register('reads', reads, args, prereqs, result)

def reads(node):
	if isinstance(node, Module):
		print(node)
	
	for child in node:
		reads(child)
	
	if isinstance(node, Assign):
		#~print("In assignment {0}".format(node))
		
		if isinstance(node.var, Name):
			sym = node.var.symbol
		else:
			sym = node.var.name.symbol
		
		sym['reads'] = 0
	
	elif isinstance(node, Name):
		#~print("In read of symbol {0}".format(node.symbol))
		node.symbol['reads'] += 1
	
	elif isinstance(node, Subscript):
		if isinstance(node.name, Name):
			node.name.symbol['reads'] += 1
	
	elif isinstance(node, Phi):
		node.target.symbol['reads'] = 0
