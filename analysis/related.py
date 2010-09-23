"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/09/018
Description:	Finds related symbols.
"""

from lib.ast import *

def findRelatedAST(node, ig):
	if isinstance(node, Assign):
		sym0 = node.var.symbol
		sym0['related'] = None
		
		if isinstance(node.exp, Name):
			sym1 = node.exp.symbol
			
			if testSafety(node, sym0, sym1, ig):
				sym0['related'] = sym1
		
		elif isinstance(node.exp, BinOp):
			sym1 = node.exp.left.symbol
			
			if testSafety(node, sym0, sym1, ig):
				sym0['related'] = sym1
			
			else:
				if isinstance(node.exp, Add) or isinstance(node.exp, Mul):
					sym1 = node.exp.right.symbol
					
					if testSafety(node, sym0, sym1, ig):
						sym0['related'] = sym1
		
		elif isinstance(node.exp, UnaryOp) and isinstance(node.exp.operand, Name):
			sym1 = node.exp.operand.symbol
			
			if testSafety(node, sym0, sym0['related'], ig):
				sym0['related'] = sym1
	
	for child in node:
		findRelatedAST(child, ig)

def testSafety(node, sym0, sym1, ig):
	return not sym1 in node['post-alive'] and len(ig[sym0] | ig[sym1]) == len(ig[sym0])
