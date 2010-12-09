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
result	= None
sets		= ['related', 'phi-related']

def init():
	from analysis.pass_manager import register
	register('related', related, args, prereqs, result, sets)

def related(node):
	if isinstance(node, Assign):
		sym0 = extractSymbol(node.var)
		
		sym0['related']	= set()
		sym0['phi-related']	= set()
		
		if isinstance(node.exp, Symbol):
			sym1 = node.exp
			
			if not sym1 in node['post-alive']:
				sym0['related'].add(sym1)
		
		elif isinstance(node.exp, BinOp):
			if isinstance(node.exp.left, Symbol):
				#Mark the left symbol as related to the target symbol.
				sym1 = node.exp.left
				
				if sym1 not in node['post-alive']:
					sym0['related'].add(sym1)
			
			if classGuard(node.exp, Add, Mul) and isinstance(node.exp.right, Symbol):
				#Mark the right symbol as related to the target symbol if
				#this is an Add or Mul node.
				sym1 = node.exp.right
				
				if sym1 not in node['post-alive']:
					sym0['related'].add(sym1)
		
		elif isinstance(node.exp, UnaryOp) and isinstance(node.exp.operand, Symbol):
			sym1 = node.exp.operand
			
			if not sym1 in node['post-alive']:
				sym0['related'].add(sym1)
	
	elif isinstance(node, Function):
		for sym in node.argSymbols:
			sym['related']		= set()
			sym['phi-related']	= set()
	
	elif isinstance(node, Phi):
		target = node.target
		
		target['related']		= set()
		target['phi-related']	= set()
		
		for sym0 in node:
			target['phi-related'].add(sym0)
			sym0['phi-related'].add(target)
			
			for sym1 in node:
				if sym0 != sym1:
					sym0['phi-related'].add(sym1)
	
	for child in node:
		related(child)
