"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/09/18
Description:	Finds related symbols.
"""

from lib.ast import *

args		= []
prereqs	= ['liveness', 'spans']
result	= 'relgraph'

def init():
	from analysis.pass_manager import register
	register('related', related, args, prereqs, result)

def related(node, graph = {}):
	if isinstance(node, Assign):
		sym0 = node.var.symbol
		sym0['related-backward'] = None
		graph[sym0] = []
		
		if isinstance(node.exp, Name):
			sym1 = node.exp.symbol
			
			if not sym1 in node['post-alive']:
				sym0['related-backward'] = sym1
				graph[sym1].append(sym0)
		
		elif isinstance(node.exp, BinOp):
			sym1 = None
			
			#Check the left operand.
			if isinstance(node.exp.left, Name):
				sym1 = node.exp.left.symbol
				
				if not sym1 in node['post-alive']:
					graph[sym1].append(sym0)
			
			#Check the right operand if the BinOp is an add or a multiply.
			if isinstance(node.exp.right, Name) and (isinstance(node.exp, Add) or isinstance(node.exp, Mul)):
				sym2 = node.exp.right.symbol
				
				if not sym2 in node['post-alive']:
					graph[sym2].append(sym0)
				
				#Pick the right over the left operand if it was defined
				#closer to this symbol.
				if sym1 == None or sym1['span-start'] < sym2['span-start']:
					sym1 = sym2
			
			if sym1 and not sym1 in node['post-alive']:
				sym0['related-backward'] = sym1
		
		elif isinstance(node.exp, UnaryOp) and isinstance(node.exp.operand, Name):
			sym1 = node.exp.operand.symbol
			
			if not sym1 in node['post-alive']:
				sym0['related-backward'] = sym1
				graph[sym1].append(sym0)
	
	for child in node:
		related(child)
	
	return graph
