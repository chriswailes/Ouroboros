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
	postStmts		= []
	ret			= node
	
	#Setup flattening for this node's children.
	if isinstance(node, Assign):
		newInPlace = True
	
	elif isinstance(node, BasicBlock):
		st = node.st
		newInPlace = True
	
	#Flatten each of our child nodes.
	for child in node:
		childPreStmts, newChild, childPostStmts = flatten(child, st, newInPlace)
		
		if isinstance(node, BasicBlock):
			newChildren.append(childPreStmts)
			newChildren.append(newChild)
			newChildren.append(childPostStmts)
		
		else:
			preStmts.append(childPreStmts)
			newChildren.append(newChild)
			postStmts.append(childPostStmts)
	
	#Here we do the actual flattening.
	if isinstance(ret, Expression) and not isinstance(ret, Symbol) and \
	not isinstance(ret, Literal) and not inplace:
		sym = st.getSymbol(assign = True)
		preStmts.append(Assign(sym, ret))
		
		ret = sym
	
	#Translate this node if neccessary.
	if isinstance(node, Assign):
		#Assignments to subscripts need to be flattened/translated into
		#function calls.
		if isinstance(node.var, Subscript):
			funName = st.getName('set_subscript')
			ret = FunctionCall(funName, [node.var.symbol, node.var.subscript, node.exp])
		
		#The assignment of dictionaries or lists to variables needs to be
		#flattened/translated.
		if isinstance(node.exp, Dictionary):
			node.exp = FunctionCall(st.getName('create_dict'))
			
			name = st.getName('set_subscript')
			for child in node.exp:
				fn = FunctionCall(name, [node.var, child, exp.value[child]])
				postStmts.append(fn)
		
		elif isinstance(node.exp, List):
			node.exp = FunctionCall(st.getName('create_list'), [Integer(len(exp.elements))])
			
			index = 0
			name = st.getFunSymbol('set_subscript')
			for child in node.exp:
				fn = FunctionCall(name, [node.var, Integer(index), child])
				postStmts.append(fn)
				
				index += 1
	
	elif isinstance(node, IfExp):
		#Create the new If node's Join node.
		jn = Join()
		
		#Create the then clause's symbol table, update the Join node, and create
		#the then clause proper.
		stThen = SymbolTable(st)
		
		name = stThen.getSymbol(assign = True)
		jn.addName(name, stThen)
		
		then = BasicBlock([Assign(name, node.then)], stThen)
		
		#Create the else clause's symbol table, update the Join node, and create
		#the else clause proper.
		stEls = SymbolTable(st)
		stEls.update(stThen)
		
		name = stEls.getSymbol(assign = True)
		jn.addName(name, stEls)
		
		els = BasicBlock([Assign(name, node.els)], stEls)
		
		#Updte our SymbolTable (this should have no effect as statements
		#aren't allowed in IfExp nodes).
		st.update(stEls)
		st.update(jn)
		
		#Append this new If node to our pre-statements and then replace the
		#node with the target from the join node's (hopefully) only Phi node.
		preStmts.append(If(node.cond, then, els, jn))
		ret = jn.phis[0].target
	
	elif isinstance(node, Subscript):
		#If there is a read from a subscript it needs to be replaced with a
		#function call.
		funName = st.getName('get_subscript')
		ret = FunctionCall(funName, [node.symbol, node.subscript])
	
	#Flatten our list of pre and post-statements and new child nodes.
	newChildren = util.flatten(newChildren)
	preStmts = util.flatten(preStmts)
	postStmts = util.flatten(postStmts)
	
	#Set our new child nodes.
	node.setChildren(newChildren)
	
	return ret if isinstance(node, Module) else (preStmts, ret, postStmts)
