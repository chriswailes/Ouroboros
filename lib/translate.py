"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/08/23
Description:	A function for converting from the compile module's AST into the
			pycom AST.
"""

import compiler
import compiler.ast as oast

import ast
import util

from symbol_table import SymbolTable

def translate(node, st = None, jn = None, funcName = False):
	if isinstance(node, oast.Add):
		left = translate(node.left, st, jn)
		right = translate(node.right, st, jn)
		
		return ast.Add(left, right)
	
	elif isinstance(node, oast.Assign):
		#Translate the right hand side first so it can use the older version
		#of the left hand side.
		expr = translate(node.expr, st, jn)
		name = translate(node.nodes.pop(), st, jn)
		
		if jn:
			#Add this new assignment to the join node.
			jn.addSymbol(name.name, st)
		
		return ast.Assign(name, expr)
	
	elif isinstance(node, oast.AssName):
		name = st.getSymbol(node.name, True)
		return ast.Name(name)
	
	elif isinstance(node, oast.CallFunc):
		name = translate(node.node, st, jn, True)
		args = [translate(a, st, jn) for a in node.args]
		
		return ast.FunctionCall(name, args)
	
	elif isinstance(node, oast.Const):
		return ast.Integer(node.value)
	
	elif isinstance(node, oast.Discard):
		return translate(node.expr, st, jn)
	
	elif isinstance(node, oast.Div):
		left = translate(node.left, st, jn)
		right = translate(node.right, st, jn)
		
		return ast.Div(left, right)
	
	elif isinstance(node, oast.If):
		tests = node.tests
		cond, then = tests.pop(0)
		
		cond = translate(cond, st)
		
		#Create our join node.
		jn = ast.Join()
		
		#A new SymbolTable needs to be constructed for the then branch.
		stThen = SymbolTable(st)
		then = ast.BasicBlock(translate(then, stThen, jn), stThen)
		
		#Merge any Join nodes in the then clause into our current Join node.
		mergeJoins(jn, then)
		
		els = None
		
		#A new SymbolTable needs to be constructed for the else branch.
		stElse = SymbolTable(st)
		#The SymbolTable needs to be updated to the new assignment versions.
		stElse.update(stThen)
		
		if len(tests) > 0:
			els = [translate(oast.If(tests, node.else_), stElse, jn)]
		else:
			els = translate(node.else_, stElse, jn)
		
		els = ast.BasicBlock(els, stElse)
		
		#Merge any Join nodes in the els clause into our current Join node.
		mergeJoins(jn, els)
		
		#Update the current SymbolTable
		st.update(stElse)
		st.update(jn)
		
		return ast.If(cond, then, els, jn)
		
	elif isinstance(node, oast.Module):
		#Create a new SymbolTable for this module.
		st = SymbolTable()
		children = ast.BasicBlock(translate(node.node, st, jn), st)
		
		return ast.Module(children)
	
	elif isinstance(node, oast.Mul):
		left = translate(node.left, st, jn)
		right = translate(node.right, st, jn)
		
		return ast.Mul(left, right)
	
	elif isinstance(node, oast.Name):
		name = node.name
		if not funcName:
			name = st.getSymbol(name)
		
		return ast.Name(name)
		
	elif isinstance(node, oast.Printnl):
		children = util.flatten([translate(e, st, jn) for e in node.getChildNodes()])
		
		return ast.FunctionCall(ast.Name("print_int_nl"), children)
		
	elif isinstance(node, oast.Stmt):
		stmts = [translate(s, st, jn) for s in node.getChildNodes()]
		
		return util.flatten(stmts)
	
	elif isinstance(node, oast.Sub):
		left = translate(node.left, st, jn)
		right = translate(node.right, st, jn)
		
		return ast.Sub(left, right)
		
	elif isinstance(node, oast.UnarySub):
		operand = translate(node.expr, st, jn)
		
		return ast.Negate(operand)
	
	else:
		None

def mergeJoins(jn0, block):
	for n in block:
		if isinstance(n, ast.If):
			for t in n.jn.getTargets():
				#Symbols that don't exist in the scope of jn0 won't be added
				#because we don't provide a StateTable to addSymbol.
				jn0.addSymbol(t)
