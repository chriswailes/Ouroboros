"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/10/07
Description:	A transformation that make sure there are only simple nodes in
			the AST.
"""

from lib.ast import *
from lib import util

analysis	= []
args		= []

def init():
	from transforms.pass_manager import register
	register('simplify', simplify, analysis, args)

def simplify(node, st = None):
	postStmts = []
	
	if isinstance(node, Assign):
		var = node.var
		exp = node.exp
		
		if isinstance(exp, List):
			name = Name(st.getFunSymbol('create_list'))
			node.exp = FunctionCall(name, [Integer(len(exp.elements))])
			
			index = 0
			name = Name(st.getFunSymbol('set_subscript'))
			for child in exp:
				fn = FunctionCall(name, [node.var, Integer(index), child])
				postStmts.append(fn)
				
				index += 1
		
		elif isinstance(exp, Dictionary):
			name = Name(st.getFunSymbol('create_dict'))
			node.exp = FunctionCall(name)
			
			name = Name(st.getFunSymbol('set_subscript'))
			for child in exp.pairs:
				fn = FunctionCall(name, [node.var, child, exp.pairs[child]])
				postStmts.append(fn)
	
	elif isinstance(node, BasicBlock):
		st = node.st
		newChildren = []
		
		for child in node:
			newChild, postStmts = simplify(child, st)
			
			newChildren.append(newChild)
			newChildren.append(postStmts)
		
		node.children = util.flatten(newChildren)
	
	else:
		for child in node:
			simplify(child, st)
	
	return node, util.flatten(postStmts)
