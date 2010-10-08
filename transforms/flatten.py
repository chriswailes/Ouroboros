"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/09/01
Description:	A transformation that flattens the provided AST.
"""

from lib.ast import *
from lib import util

from lib.symbol_table import SymbolTable

analysis	= []
args		= []

def init():
	from transforms.pass_manager import register
	register('flatten', flatten, analysis, args)

def flatten(node, st = None, inplace = False):
	newChildren	= []
	newInPlace	= False
	preStmts		= []
	ret			= node
	
	if isinstance(node, Assign):
		newInPlace = True
	
	elif isinstance(node, BasicBlock):
		st = node.st
		newInPlace = True
	
	for child in node:
		childPreStmts, newChild = flatten(child, st, newInPlace)
		
		if isinstance(node, BasicBlock):
			newChildren.append(childPreStmts)
			newChildren.append(newChild)
		
		else:
			preStmts.append(childPreStmts)
			newChildren.append(newChild)
	
	#Flatten our collections.
	newChildren = util.flatten(newChildren)
	preStmts = util.flatten(preStmts)
	
	#Set our children.
	node.setChildren(newChildren)
	
	if isinstance(node, Assign) and isinstance(node.var, Subscript):
		funName = Name(st.getFunSymbol('set_subscript'))
		ret = FunctionCall(funName, [node.var.name, node.var.subscript, node.exp])
	
	elif (isinstance(node, UnaryOp) or isinstance(node, BinOp) or isinstance(node, FunctionCall)) and not inplace:
		ret = Name(st.getSymbol(assign = True))
		preStmts.append(Assign(ret, node))
	
	elif isinstance(node, List) or isinstance(node, Dictionary):
		ret = Name(st.getSymbol(assign = True))
		preStmts.append(Assign(ret, node))
	
	elif isinstance(node, Subscript):
		funName = Name(st.getFunSymbol('get_subscript'))
		funCall = FunctionCall(funName, [node.name, node.subscript])
		
		if inplace:
			ret = funCall
		
		else:
			ret = Name(st.getSymbol(assign = True))
			preStmts.append(Assign(ret, funCall))
	
	elif isinstance(node, IfExp):
		
		jn = Join()
		
		stThen = SymbolTable(st)
		name = Name(stThen.getSymbol(assign = True))
		jn.addName(name, stThen)
		
		then = BasicBlock([Assign(name, node.then)], stThen)
		
		stEls = SymbolTable(st)
		stEls.update(stThen)
		name = Name(stEls.getSymbol(assign = True))
		jn.addName(name, stEls)
		
		els = BasicBlock([Assign(name, node.els)], stEls)
		
		st.update(stEls)
		st.update(jn)
		
		preStmts.append(If(node.cond, then, els, jn))
		ret = jn.phis[0].target
	
	if isinstance(node, Module):
		return ret
	
	else:
		return preStmts, ret
