"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/09/01
Description:	A transformation that flattens the provided AST.
"""

from assembler.tagging import OBJ

from lib.ast import *
from lib import util

from lib.symbol_table import SymbolTable, getSingleton

analysis	= ['heapify']
args		= []

def init():
	from transforms.pass_manager import register
	register('flatten', flatten, analysis, args)

def flatten(node, st = None, inPlace = False):
	newChildren	= []
	newInPlace	= None
	preStmts		= []
	
	#Setup flattening for this node's children.
	if util.classGuard(node, Assign, BasicBlock, Module):
		newInPlace = node.__class__
	
		if isinstance(node, BasicBlock):
			st = node.st
	
	#Flatten each of our child nodes.  Dictionaries, if-expressions, and lists
	#do their own flattening.
	if not classGuard(node, Dictionary, IfExp, List):
		for child in node:
			childPreStmts, newChild = flatten(child, st, newInPlace)
			
			if isinstance(node, BasicBlock):
				newChildren.append(childPreStmts)
				newChildren.append(newChild)
			
			else:
				preStmts.append(childPreStmts)
				newChildren.append(newChild)
		
		#Set our new child nodes.
		newChildren = util.flatten(newChildren)
		node.setChildren(newChildren)
	
	#Translate this node if neccessary.
	if isinstance(node, Assign):
		#Assignments to subscripts need to be flattened/translated into
		#function calls.
		if isinstance(node.var, Subscript):
			funName = st.getName('set_subscript')
			node = FunctionCall(funName, node.var.symbol, node.var.subscript, node.exp)
	
	elif isinstance(node, Dictionary):
		pairs = node.value
		
		node = FunctionCall(st.getName('create_dict'))
		node.tag = OBJ
		
		sym = st.getSymbol(assign = True)
		preStmts.append(Assign(sym, node))
		node = sym
		
		name = st.getName('set_subscript')
		for key in pairs:
			#Flatten the key
			childPreStmts, key = flatten(key, st)
			preStmts.append(childPreStmts)
			
			#Flatten the value
			childPreStmts, value = flatten(pairs[key], st)
			preStmts.append(childPreStmts)
			
			#Add the key/value pair to the dictionary.
			preStmts.append(FunctionCall(name, sym, key, value))
	
	elif isinstance(node, IfExp):
		#Create the new If node's Join node.
		jn = Join()
		
		#Flattent he conditional expression.
		condPreStmts, cond = flatten(node.cond, st, jn)
		preStmts.append(condPreStmts)
		
		#Create the assignment variable for the then clause.
		sym = st.getSymbol(assign = True)
		jn.addSymbol(sym, st)
		
		_, then = flatten(BasicBlock([Assign(sym, node.then)], st))
		
		#Create the assignment variable for the else clause.
		sym = st.getSymbol(assign = True)
		jn.addSymbol(sym, st)
		
		_, els = flatten(BasicBlock([Assign(sym, node.els)], st))
		
		#Updte our SymbolTable (this should have no effect as statements
		#aren't allowed in IfExp nodes).
		st.update(jn)
		
		#Append this new If node to our pre-statements and then replace the
		#node with the target from the join node's (hopefully) only Phi node.
		preStmts.append(If(cond, then, els, jn))
		node = jn.phis[0].target
	
	elif isinstance(node, List):
		children = node.value
		
		node = FunctionCall(st.getName('create_list'), Integer(len(node.value)))
		node.tag = OBJ
		
		sym = st.getSymbol(assign = True)
		preStmts.append(Assign(sym, node))
		node = sym
			
		index = 0
		name = st.getName('set_subscript')
		for child in children:
			#Flatten the value.
			childPreStmts, newChild = flatten(child, st)
			preStmts.append(childPreStmts)
			
			#Add the value to the list.
			preStmts.append(FunctionCall(name, sym, Integer(index), newChild))
			
			index += 1
	
	elif isinstance(node, Subscript):
		#If there is a read from a subscript it needs to be replaced with a
		#function call.
		funName = st.getName('get_subscript')
		node = FunctionCall(funName, node.symbol, node.subscript)
	
	#Here we do the actual flattening.
	if classGuard(node, BinOp, FunctionCall, IfExp, UnaryOp) and not inPlace:
		sym = st.getSymbol(assign = True)
		preStmts.append(Assign(sym, node))
		
		node = sym
	
	elif isinstance(node, Function) and inPlace != Module:
		closured = []
		
		print("Flattening {0}".format(node.name))
		
		for sym in node['free']:
			if sym['heapify'] == 'closure':
				closured.append(sym)
				node.argSymbols.append(sym)
		
		#Remove the variables that we have put into the closure from the list
		#of free variables for this function.
		node['free'] -= set(closured)
		
		preStmts.append(node)
		
		if len(closured) > 0:
			node = FunctionCall(Name('create_closure'), node.name, List(closured))
		
		else:
			node = node.name
	
	#Flatten our list of pre-statements.
	preStmts = util.flatten(preStmts)
	
	return node if isinstance(node, Module) else (preStmts, node)
