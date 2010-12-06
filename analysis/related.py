"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/09/18
Description:	Finds related symbols.
"""

from lib.ast import *
from lib.util import extractSymbol

args		= []
prereqs	= ['liveness', 'spans']
result	= 'relgraph'
sets		= ['related-backward', 'phi-related']

def init():
	from analysis.pass_manager import register
	register('related', related, args, prereqs, result, sets)

def related(node, graph = {}):
	if isinstance(node, Assign):
		sym0 = extractSymbol(node.var)
		
		sym0['related-backward'] = None
		sym0['phi-related'] = []
		graph[sym0] = []
		
		if isinstance(node.exp, Symbol):
			sym1 = node.exp
			
			if not sym1 in node['post-alive']:
				sym0['related-backward'] = sym1
				graph[sym1].append(sym0)
		
		elif isinstance(node.exp, BinOp):
			sym1 = None
			
			#Check the left operand.
			if isinstance(node.exp.left, Symbol):
				sym1 = node.exp.left
				
				if sym1 not in node['post-alive'] and sym0 not in graph[sym1]:
					graph[sym1].append(sym0)
			
			#Check the right operand if the BinOp is an add or a multiply.
			if classGuard(node.exp, Add, Mul) and isinstance(node.exp.right, Symbol):
				sym2 = node.exp.right
				
				if sym2 not in node['post-alive'] and sym0 not in graph[sym2]:
					graph[sym2].append(sym0)
				
				#Pick the right over the left operand if it was defined
				#closer to this symbol.
				if sym1 == None or sym1['span-start'] < sym2['span-start']:
					sym1 = sym2
			
			if sym1 and not sym1 in node['post-alive']:
				sym0['related-backward'] = sym1
		
		elif isinstance(node.exp, UnaryOp) and isinstance(node.exp.operand, Symbol):
			sym1 = node.exp.operand
			
			if not sym1 in node['post-alive']:
				sym0['related-backward'] = sym1
				graph[sym1].append(sym0)
	
	elif isinstance(node, Function):
		for sym in node.argSymbols:
			sym['related-backward'] = None
			sym['phi-related'] = []
			graph[sym] = []
	
	elif isinstance(node, Phi):
		node.target['phi-related'] = []
		graph[node.target] = []
		
		for sym0 in node:
			node.target['phi-related'].append(sym0)
			
			sym0['phi-related'].append(node.target)
			
			for sym1 in node:
				sym0['phi-related'].append(sym1)
	
	for child in node:
		related(child)
	
	return graph
