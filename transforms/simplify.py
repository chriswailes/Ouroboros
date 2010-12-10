"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		Ouroboros
Date:		2010/09/01
Description:	A transformation that simplifies non-simple nodes.
"""

from assembler.tagging import OBJ

from lib.ast import *
from lib import util

from lib.symbol_table import SymbolTable

analysis	= ['liveness', 'heapify']
args		= []

def init():
	from transforms.pass_manager import register
	register('simplify', simplify, analysis, args)

def simplify(node, st = None):
	newChildren	= []
	preStmts		= []
	st			= node.st if isinstance(node, Function) else st
	
	##############################
	# Pre-simplification Clauses #
	##############################
	
	if isinstance(node, IfExp):
		#Simplify he conditional expression.
		condPreStmts, cond = simplify(node.cond, st)
		preStmts.append(condPreStmts)
		
		#Create the assignment variable for the different clauses.
		sym0 = st.getTemp()
		sym1 = st.getSymbol(sym0.name, True)
		
		#Build our new nodes.
		then = BasicBlock([Assign(sym0, node.then)])
		els  = BasicBlock([Assign(sym1, node.els )])
		
		_, if_  = simplify(If(cond, then, els, st), st)
		
		#Append this new If node to our pre-statements and then replace the
		#node with the target from the join node's only Phi node.
		preStmts.append(if_)
		node = if_.jn.phis[0].target
	
	#Simplify the children of this node.
	for child in node:
		childPreStmts, newChild = simplify(child, st)
			
		if isinstance(node, BasicBlock):
			newChildren.append(childPreStmts)
			newChildren.append(newChild)
		
		else:
			preStmts.append(childPreStmts)
			newChildren.append(newChild)

	#Set the node's new children.
	newChildren = util.flatten(newChildren)
	node.setChildren(newChildren)
	
	#Post-simplification clauses.
	if isinstance(node, Assign) and isinstance(node.var, Subscript):
		node = FunctionCall(st.getBIF('set_subscript'), node.var.symbol, node.var.subscript, node.exp)
	
	elif isinstance(node, Dictionary):
		fun = FunctionCall(st.getBIF('create_dict'))
		fun.tag = OBJ
		
		sym = st.getTemp()
		preStmts.append(Assign(sym, fun))
		
		name = st.getBIF('set_subscript')
		for key in node.value:
			#Add the key/value pair to the dictionary.
			preStmts.append(FunctionCall(name, sym, key, node.value[key]))
		
		#Replace this node with the symbol that now holds the dictionary.
		node = sym
	
	elif isinstance(node, Function) and not node['simplified']:
		closure = []
		
		#Mark this node as having been simplified.
		node['simplified'] = True
		
		for sym in node['free']:
			if sym['heapify'] == 'closure':
				closure.append(sym)
		
		#Remove the variables that we have put into the closure from the list
		#of free variables for this function.
		node['free'] -= set(closure)
		
		preStmts.append(node)
		
		if len(closure) > 0:
			closureSym = st.getSymbol('!closure', True)
			node.argSymbols.insert(0, closureSym)
			
			#Set up our callTest, substituteTest, and replacement lambda.
			callTest		= lambda node: True
			substituteTest	= lambda node: isinstance(node, Symbol) and node in closure
			replacement	= lambda node: Subscript(closureSym, Integer(closure.index(node)))
			
			util.substitute(node, callTest, substituteTest, replacement)
			
			node = FunctionCall(st.getBIF('create_closure'), node.name, List(closure))
			node.tag = OBJ
		
		else:
			node = node.name
	
	elif isinstance(node, GetAttr):
		node = FunctionCall(st.getBIF('get_attr'), node.exp, node.attrName)
	
	elif isinstance(node, List):
		fun = FunctionCall(st.getBIF('create_list'), Integer(len(node.value)))
		fun.tag = OBJ
		
		sym = st.getTemp()
		preStmts.append(Assign(sym, fun))
		
		name = st.getBIF('set_subscript')
		for index in range(0, len(node.value)):
			preStmts.append(FunctionCall(name, sym, Integer(index), node.value[index]))
		
		#Replace this node with the symbol that now holds the list.
		node = sym
	
	elif isinstance(node, SetAttr):
		node = FunctionCall(st.getBIF('set_attr'), node.exp, node.attrName, node.value)
	
	elif isinstance(node, Subscript):
		#If there is a read from a subscript it needs to be replaced with a
		#function call.
		funName = st.getBIF('get_subscript')
		node = FunctionCall(funName, node.symbol, node.subscript)
	
	#Flatten our list of pre-statements.
	preStmts = util.flatten(preStmts)
	
	return node if isinstance(node, Module) else (preStmts, node)
