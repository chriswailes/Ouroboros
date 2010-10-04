"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/10/04
Description:	An analysis that does some simple typification at compile time.
"""

from lib.ast import *

args		= []
prereqs	= []
result	= None

def init():
	from analysis.pass_manager import register
	register('typify', typify, args, prereqs, result)

def typify(node):
	if isinstance(node, Assign):
		#~if isinstance(node.exp, Integer):
			#~node['type'] = Integer
		#~
		#~elif isinstance(node.exp, Boolean):
			#~node['type'] = Boolean
		#~
		#~else:
			#~node['type'] = Value
		
		node['type'] = Integer
	
	for child in node:
		typify(child)
