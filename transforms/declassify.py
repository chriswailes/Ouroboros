"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/09/01
Description:	A transformation that transforms a class definition into simple
			AST nodes.
"""

from assembler.tagging import BOOL, OBJ

from lib.ast import *
from lib import util

from lib.symbol_table import SymbolTable

analysis	= []
args		= []

def init():
	from transforms.pass_manager import register
	register('declassify', declassify, analysis, args)

def declassify(node, st = None, strings = None, klass = None):
	newChildren	= []
	preStmts		= []
	st			= node.st if isinstance(node, Function) else st
	strings		= node.strings if isinstance(node, Module) else strings
	
	if isinstance(node, Class):
		sym = st.getSymbol(assign = True)
		
		fun = FunctionCall(st.getName('create_class'), List(node.bases))
		fun.tag = OBJ
		
		preStmts.append(Assign(sym, fun))
		
		_, body = declassify(node.body, st, strings, sym)
		
		preStmts.append(body)
		
		node = sym
	
	elif isinstance(node, Assign) and klass:
		string = node.var.name
		string = strings.setdefault(string, String(string))
		
		#~sym = st.getSymbol()
		
		node = SetAttr(klass, string, node.exp)
	
	elif isinstance(node, FunctionCall):
		if isinstance(node.name, Symbol) and node.name.has_key('type') and node.name['type'] == 'class':
			sym = st.getSymbol(assign = True)
			string = strings.setdefault('__init__', String('__init__'))
			
			base = node.name
			fun = FunctionCall(st.getName('create_object'), base)
			fun.tag = OBJ
			
			preStmts.append(Assign(sym, fun))
			
			cond = FunctionCall(st.getName('has_attr'), base, string)
			cond.tag = BOOL
			
			then = BasicBlock([FunctionCall(GetAttr(base, string), sym, *node.args)])
			els_ = BasicBlock([])
			
			preStmts.append(If(cond, then, els_, Join()))
			
			node = sym
		
		elif isinstance(node.name, GetAttr) and not node.name.exp.has_key('type'):
			node.args.insert(0, node.name.exp)
	
	if not isinstance(node, Class):
		#Declassify the children of this node.
		for child in node:
			childPreStmts, newChild = declassify(child, st, strings, klass)
				
			if isinstance(node, BasicBlock):
				newChildren.append(childPreStmts)
				newChildren.append(newChild)
			
			else:
				preStmts.append(childPreStmts)
				newChildren.append(newChild)
		
		#Set the node's new children.
		newChildren = util.flatten(newChildren)
		node.setChildren(newChildren)
	
	if isinstance(node, Module):
		node.strings = strings
	
	return node if isinstance(node, Module) else (preStmts, node)

def simplifyClassBody(node, klass, st, assigned = []):
	if isinstance(node, BasicBlock):
		assigned = node.collectSymbols('w')
	
	if not isinstance(node, Function):
		node.setChildren([simplifyClassBody(child, klass, st, assigned) for child in node])
	
	if isinstance(node, Assign):
		node = FunctionCall(st.getName('set_attr'), klass, node.var, node.exp)
	
	elif isinstance(node, Symbol):
		pass
	
	return node
