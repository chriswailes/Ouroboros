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
	for child in node:
		reads(child)
	
	if isinstance(node, Assign):
		sym = node.var.sybmol if isinstance(node.var, Subscript) else node.var
		#~print("In assignment for {0}".format(sym))
		sym['reads'] = 0
	
	elif isinstance(node, Phi):
		node.target['reads'] = 0
	
	elif isinstance(node, Symbol):
		#~print("Reading {0}".format(node))
		node['reads'] += 1
	
	#This little hack is here to take care of cases where subscripts are
	#applied to literal values. After the flatten transformation this branch
	#will be taken whenever we see a subscript.
	elif isinstance(node, Subscript) and isinstance(node.symbol, Symbol):
		node.symbol['reads'] += 1
