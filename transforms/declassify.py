"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/09/01
Description:	A transformation that transforms a class definition into simple
			AST nodes.
"""

from assembler.tagging import OBJ

from lib.ast import *
from lib import util

from lib.symbol_table import SymbolTable

analysis	= []
args		= []

def init():
	from transforms.pass_manager import register
	register('declassify', declassify, analysis, args)

def declassify(tree):
	if isinstance(node, Class):
		sym = st.getSymbol(assign = True)
		
		fun = FunctionCall(st.getName('create_class'), List(node.bases))
		fun.tag = OBJ
		
		preStmts.append(Assign(sym, fun))
		
		#Generate body.
		preStmts.append(simplifyClassBody(node.body, sym, st))
		
		node = sym

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
