"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/09/018
Description:	Finds related symbols.
"""

from lib.ast import *

def findRelatedAST(node):
	if isinstance(node, Assign):
		sym0 = node.var.symbol
		
		if isinstance(node.exp, Name):
			sym1 = node.exp.symbol
			
			if not sym1 in node['post-alive']:
				sym0['related'] = sym1
		
		if not sym0.has_key('related'):
			sym0['related'] = None
	
	for child in node:
		findRelatedAST(child)
