"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/09/18
Description:	Finds related symbols.
"""

from lib.ast import *

args		= ['ig']
prereqs	= ['interference', 'liveness']
result	= None

def init():
	from analysis.pass_manager import register
	register('related', related, args, prereqs, result)

def related(node, ig):
	if isinstance(node, Assign):
		sym0 = node.var.symbol
		sym0['related'] = None
		
		if isinstance(node.exp, Name):
			sym1 = node.exp.symbol
			
			if not sym1 in node['post-alive']:
				sym0['related'] = sym1
		
		elif isinstance(node.exp, BinOp):
			sym1 = None
			
			if isinstance(node.exp.left, Name):
				sym1 = node.exp.left.symbol
			
			elif isinstance(node.exp.right, Name) and (isinstance(node.exp, Add) or isinstance(node.exp, Mul)):
				sym1 = node.exp.right.symbol
			
			if sym1 and not sym1 in node['post-alive']:
				sym0['related'] = sym1
		
		elif isinstance(node.exp, UnaryOp) and isinstance(node.exp.operand, Name):
			sym1 = node.exp.operand.symbol
			
			if not sym1 in node['post-alive']:
				sym0['related'] = sym1
	
	for child in node:
		findRelated(child, ig)
			
