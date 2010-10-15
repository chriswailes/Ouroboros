"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/09/01
Description:	A transformation that flattens the provided AST.
"""

from assembler.tagging import OBJ

from lib.ast import *
from lib import util

from lib.symbol_table import SymbolTable

analysis	= []
args		= []

def init():
	from transforms.pass_manager import register
	register('flatten', flatten, analysis, args)

def flatten(node, st = None, inPlace = False):
	newChildren	= []
	newInPlace	= False
	preStmts		= []
	postStmts		= []
	
	#Setup flattening for this node's children.
	if isinstance(node, Assign):
		newInPlace = util.extractSymbol(node.var)
	
	elif isinstance(node, BasicBlock):
		st = node.st
		newInPlace = True
	
	#Flatten each of our child nodes.  Dictionaries and lists do their own
	#flattening.
	if not classGuard(node, Dictionary, List):
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
		
		if inPlace:
			sym = inPlace
			stmts = postStmts
		
		else:
			sym = st.getSymbol(assign = True)
			preStmts.append(Assign(sym, node))
			node = sym
			
			stmts = preStmts
		
		name = st.getName('set_subscript')
		for key in pairs:
			#Flatten the key
			childPreStmts, key, childPostStmts = flatten(key, st)
			
			stmts.append(childPreStmts)
			stmts.append(childPostStmts)
			
			#Flatten the value
			childPreStmts, value, childPostStmts = flatten(pairs[key], st)
			
			stmts.append(childPreStmts)
			stmts.append(childPostStmts)
			
			#Add the key/value pair to the dictionary.
			stmts.append(FunctionCall(name, sym, key, value))
	
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
		node = jn.phis[0].target
	
	elif isinstance(node, List):
		children = node.value
		
		node = FunctionCall(st.getName('create_list'), Integer(len(node.value)))
		node.tag = OBJ
		
		if inPlace:
			sym = inPlace
			stmts = postStmts
		
		else:
			sym = st.getSymbol(assign = True)
			preStmts.append(Assign(sym, node))
			node = sym
			
			stmts = preStmts
		
		index = 0
		name = st.getName('set_subscript')
		for child in children:
			#Flatten the value.
			childPreStmts, newChild, childPostStmts = flatten(child, st)
			
			stmts.append(childPreStmts)
			stmts.append(childPostStmts)
			
			#Add the value to the list.
			stmts.append(FunctionCall(name, sym, Integer(index), newChild))
			
			index += 1
	
	elif isinstance(node, Subscript):
		#If there is a read from a subscript it needs to be replaced with a
		#function call.
		funName = st.getName('get_subscript')
		node = FunctionCall(funName, node.symbol, node.subscript)
	
	#Here we do the actual flattening.
	if isinstance(node, Expression) and not classGuard(node, Integer, Boolean, Symbol) and not inPlace:
		sym = st.getSymbol(assign = True)
		preStmts.append(Assign(sym, node))
		
		node = sym
	
	#Flatten our list of pre and post-statements.
	preStmts = util.flatten(preStmts)
	postStmts = util.flatten(postStmts)
	
	return node if isinstance(node, Module) else (preStmts, node, postStmts)
