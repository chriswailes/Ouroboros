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
		countReads(child)
	
	if isinstance(node, Assign):
		node.var.symbol['reads'] = 0
	
	elif isinstance(node, Name):
		node.symbol['reads'] += 1
