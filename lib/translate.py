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

def translate(node, st = None, strings = None, jn = None, funcName = False):
	if isinstance(node, oast.Add):
		left = translate(node.left, st, strings, jn)
		right = translate(node.right, st, strings, jn)
		
		return ast.Add(left, right)
	
	elif isinstance(node, oast.And):
		left = translate(node.nodes[0], st, strings, jn)
		right = translate(node.nodes[1], st, strings, jn)
		
		return ast.And(left, right)
	
	elif isinstance(node, oast.Assign):
		#Translate the right hand side first so it can use the older version
		#of the left hand side.
		exp	= translate(node.expr, st, strings, jn)
		var = node.nodes.pop()
		
		if isinstance(var, oast.AssAttr):
			string = strings.setdefault(var.attrname, ast.String(var.attrname))
			var = translate(var.expr, st, strings, jn)
			
			return ast.SetAttr(var, string, exp)
		
		else:
			var	= translate(var, st, strings, jn)
			
			if jn != None:
				#Add this new assignment to the join node.
				jn.addSymbol(var, st)
			
			return ast.Assign(var, exp)
	
	elif isinstance(node, oast.AssName):
		return st.getSymbol(node.name, True)
	
	elif isinstance(node, oast.CallFunc):
		name = translate(node.node, st, strings, jn, True)
		args = [translate(a, st, strings, jn) for a in node.args]
		
		return ast.FunctionCall(name, *args)
	
	elif isinstance(node, oast.Class):
		sym = st.getSymbol(node.name, True)
		name = st.getName(node.name, False, True)
		
		#This is here temporarily.  It will be moved to the typify pass later.
		sym['type'] = 'class'
		
		bases = [translate(base, st, strings, jn) for base in node.bases]
		body = ast.BasicBlock(translate(node.code, st, strings, jn))
		
		klass = ast.Class(name, bases, body)
		
		return ast.Assign(sym, klass)
	
	elif isinstance(node, oast.Compare):
		left = translate(node.expr, st, strings, jn)
		
		op, right = node.ops[0]
		
		right = translate(right, st, strings, jn)
		
		if op == '==':
			return ast.Eq(left, right)
		
		elif op == '!=':
			return ast.Ne(left, right)
		
		elif op == 'is':
			return ast.Is(left, right)
	
	elif isinstance(node, oast.Const):
		return ast.Integer(node.value)
	
	elif isinstance(node, oast.Dict):
		pairs = {}
		
		for pair in node.items:
			key, value = pair
			
			key = translate(key, st, strings, jn)
			value = translate(value, st, strings, jn)
			
			pairs[key] = value
		
		return ast.Dictionary(pairs)
	
	elif isinstance(node, oast.Discard):
		return translate(node.expr, st, strings, jn)
	
	elif isinstance(node, oast.Div):
		left = translate(node.left, st, strings, jn)
		right = translate(node.right, st, strings, jn)
		
		return ast.Div(left, right)
	
	elif isinstance(node, oast.Function):
		sym = st.getSymbol(node.name, True)
		name = st.getName(node.name, False, True)
		
		newST = SymbolTable(st)
		
		argSymbols = [newST.getSymbol(argName, True) for argName in node.argnames]
		
		block = ast.BasicBlock(translate(node.code, newST, strings, jn))
		
		fun = ast.Function(name, argSymbols, block, newST)
		fun['simplified'] = False
		
		st.update(newST)
		
		return ast.Assign(sym, fun)
	
	elif isinstance(node, oast.Getattr):
		exp = translate(node.expr, st, strings, jn)
		name = strings.setdefault(node.attrname, ast.String(node.attrname))
		
		return ast.GetAttr(exp, name)
	
	elif isinstance(node, oast.If):
		tests = node.tests
		cond, then = tests.pop(0)
		
		cond = translate(cond, st, strings)
		
		#Create our join node.
		jn = ast.Join()
		
		#A new SymbolTable needs to be constructed for the then branch.
		stThen = SymbolTable(st)
		then = ast.BasicBlock(translate(then, stThen, strings, jn))
		
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
			els = translate(node.else_, stElse, strings, jn)
		
		els = ast.BasicBlock(els)
		
		#Merge any Join nodes in the els clause into our current Join node.
		mergeJoins(jn, els)
		
		#Update the current SymbolTable
		st.update(stElse)
		st.update(jn)
		
		return ast.If(cond, then, els, jn)
	
	elif isinstance(node, oast.IfExp):
		cond = translate(node.test, st, strings, jn)
		then = translate(node.then, st, strings, jn)
		els = translate(node.else_, st, strings, jn)
		
		return ast.IfExp(cond, then, els)
	
	elif isinstance(node, oast.Lambda):
		name = st.getName('lambda', False, True)
		
		newST = SymbolTable(st)
		
		argSymbols = map(lambda name: newST.getSymbol(name, True), node.argnames)
		
		code  = ast.Return(translate(node.code, newST, strings, jn))
		block = ast.BasicBlock([code])
		fun   = ast.Function(name, argSymbols, block, newST)
		fun['simplified'] = False
		
		st.update(newST)
		
		return fun
	
	elif isinstance(node, oast.List):
		elements = []
		
		for n in node.nodes:
			elements.append(translate(n, st, strings, jn))
		
		return ast.List(elements)
		
	elif isinstance(node, oast.Module):
		#Create a new SymbolTable for this module.
		st = SymbolTable()
		strings = {}
		
		children = translate(node.node, st, strings)
		
		block = ast.BasicBlock(children)
		fun = ast.Function(st.getName('main'), [], block, st)
		
		#Mark the main function as migrated so that it doesn't get moved later.
		fun['simplified'] = True
		
		return ast.Module([fun], strings)
	
	elif isinstance(node, oast.Mul):
		left = translate(node.left, st, strings, jn)
		right = translate(node.right, st, strings, jn)
		
		return ast.Mul(left, right)
	
	elif isinstance(node, oast.Name):
		ret = 'input_int' if node.name == 'input' else node.name
		
		if ret == 'input_int':
			ret = st.getName(ret)
		
		else:
			if ret == 'True':
				ret = ast.Tru()
			
			elif ret == 'False':
				ret = ast.Fals()
			
			else:
				ret = st.getSymbol(ret)
		
		return ret
	
	elif isinstance(node, oast.Not):
		operand = translate(node.expr, st, strings, jn)
		
		return ast.Not(operand)
	
	elif isinstance(node, oast.Or):
		left = translate(node.nodes[0], st, strings, jn)
		right = translate(node.nodes[1], st, strings, jn)
		
		return ast.Or(left, right)
		
	elif isinstance(node, oast.Printnl):
		children = [translate(e, st, strings, jn) for e in node.getChildNodes()]
		children = util.flatten(children)
		
		return ast.FunctionCall(st.getName('print_any'), *children)
	
	elif isinstance(node, oast.Return):
		return ast.Return(translate(node.value, st, strings, jn))
		
	elif isinstance(node, oast.Stmt):
		stmts = [translate(s, st, strings, jn) for s in node.getChildNodes()]
		
		return util.flatten(stmts)
	
	elif isinstance(node, oast.Sub):
		left = translate(node.left, st, strings, jn)
		right = translate(node.right, st, strings, jn)
		
		return ast.Sub(left, right)
	
	elif isinstance(node, oast.Subscript):
		sym = translate(node.expr, st, strings, jn)
		sub = translate(node.subs[0], st, strings, jn)
		
		return ast.Subscript(sym, sub)
	
	elif isinstance(node, oast.While):
		jn = ast.Join()
		
		cond = translate(node.test, st, jn)
		
		if isinstance(cond, ast.Symbol):
			jn.addSymbol(cond, st)
		
		body = ast.BasicBlock(translate(node.body, st, strings, jn))
		
		return ast.While(cond, body, jn)
	
	elif isinstance(node, oast.UnarySub):
		operand = translate(node.expr, st, strings, jn)
		
		return ast.Negate(operand)
	
	else:
		None

def mergeJoins(jn, block):
	for n in block:
		if isinstance(n, ast.If):
			for t in n.jn.getTargets():
				#Symbols that don't exist in the scope of jn0 won't be added
				#because we don't provide a SymbolTable to jn.addSymbol.
				jn.addSymbol(t)
