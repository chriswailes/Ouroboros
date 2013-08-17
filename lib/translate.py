"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		Ouroboros
Date:		2010/08/23
Description:	A function for converting from the compile module's AST into the
			pycom AST.
"""

import compiler
import compiler.ast as oast

import ast
import util

from symbol_table import SymbolTable

def translate(node, st = None, strings = None, funcName = False):
	if isinstance(node, oast.Add):
		left  = translate(node.left,  st, strings, funcName)
		right = translate(node.right, st, strings, funcName)
		
		return ast.Add(left, right)
	
	elif isinstance(node, oast.And):
		left	 = translate(node.nodes[0], st, strings, funcName)
		right = translate(node.nodes[1], st, strings, funcName)
		
		return ast.And(left, right)
	
	elif isinstance(node, oast.Assign):
		# Translate the right hand side first so it can use the older version
		# of the left hand side.
		exp = translate(node.expr, st, strings, funcName)
		var = node.nodes.pop()
		
		if isinstance(var, oast.AssAttr):
			string = strings.setdefault(var.attrname, ast.String(var.attrname))
			var = translate(var.expr, st, strings, funcName)
			
			return ast.SetAttr(var, string, exp)
		
		else:
			var = translate(var, st, strings, funcName)
			
			return ast.Assign(var, exp)
	
	elif isinstance(node, oast.AssName):
		return st.getSymbol(node.name, True)
	
	elif isinstance(node, oast.CallFunc):
		name = translate(node.node, st, strings, True)
		args = [translate(a, st, strings) for a in node.args]
		
		return ast.FunctionCall(name, *args)
	
	elif isinstance(node, oast.Class):
		bases = [translate(base, st, strings, funcName) for base in node.bases]
		
		body = translate(node.code, st, strings, funcName)
		body = ast.BasicBlock(body)
		
		sym	= st.getSymbol(node.name, True)
		name	= st.getName(node.name, True)
		
		# This is here temporarily.  It will be moved to the typify pass
		# later.
		sym['type'] = 'class'
		
		klass = ast.Class(name, bases, body)
		
		return ast.Assign(sym, klass)
	
	elif isinstance(node, oast.Compare):
		left = translate(node.expr, st, strings, funcName)
		
		op, right = node.ops[0]
		
		right = translate(right, st, strings, funcName)
		
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
			
			key = translate(key, st, strings, funcName)
			value = translate(value, st, strings, funcName)
			
			pairs[key] = value
		
		return ast.Dictionary(pairs)
	
	elif isinstance(node, oast.Discard):
		return translate(node.expr, st, strings, funcName)
	
	elif isinstance(node, oast.Div):
		left  = translate(node.left,  st, strings, funcName)
		right = translate(node.right, st, strings, funcName)
		
		return ast.Div(left, right)
	
	elif isinstance(node, oast.Function):
		sym	= st.getSymbol(node.name, True)
		name	= st.getName(node.name, True)
		
		sym['type'] = 'function'
		
		newST = SymbolTable(st)
		
		argSymbols = [newST.getSymbol(argName, True) for argName in node.argnames]
		
		body = translate(node.code, newST, strings, funcName)
		body = ast.BasicBlock(body)
		
		fun = ast.Function(name, argSymbols, body, newST)
		fun['simplified'] = False
		
		st.update(newST)
		
		return ast.Assign(sym, fun)
	
	elif isinstance(node, oast.Getattr):
		exp	= translate(node.expr, st, strings, funcName)
		name	= strings.setdefault(node.attrname, ast.String(node.attrname))
		
		return ast.GetAttr(exp, name)
	
	elif isinstance(node, oast.If):
		tests = node.tests
		cond, then = tests.pop(0)
		
		# Translate the conditional expression.
		cond = translate(cond, st, strings)
		
		# Snapshot the SymbolTable
		st.snapshot()
		
		# Translate the 'then' clause.
		then = translate(then, st, strings, funcName)
		then = ast.BasicBlock(then)
		
		# Roll-back the SymbolTable for the 'else' clause.
		st.rollback()
		
		# Translate the 'else' clause.
		if len(tests) > 0:
			els = [translate(oast.If(tests, node.else_), st, funcName)]
		else:
			els = translate(node.else_, st, strings, funcName)
		
		els = ast.BasicBlock(els)
		
		return ast.If(cond, then, els, st)
	
	elif isinstance(node, oast.IfExp):
		cond = translate(node.test, st, strings, funcName)
		then = translate(node.then, st, strings, funcName)
		els = translate(node.else_, st, strings, funcName)
		
		return ast.IfExp(cond, then, els)
	
	elif isinstance(node, oast.Lambda):
		name = st.getName('lambda', True)
		
		newST = SymbolTable(st)
		
		argSymbols = map(lambda name: newST.getSymbol(name, True), node.argnames)
		
		code  = ast.Return(translate(node.code, newST, strings, funcName))
		block = ast.BasicBlock([code])
		fun   = ast.Function(name, argSymbols, block, newST)
		fun['simplified'] = False
		
		st.update(newST)
		
		return fun
	
	elif isinstance(node, oast.List):
		elements = []
		
		for n in node.nodes:
			elements.append(translate(n, st, strings, funcName))
		
		return ast.List(elements)
		
	elif isinstance(node, oast.Module):
		# Create a new SymbolTable for this module.
		st = SymbolTable()
		strings = {}
		
		children = translate(node.node, st, strings, funcName)
		
		block = ast.BasicBlock(children)
		fun = ast.Function(st.getBIF('main'), [], block, st)
		
		# Mark the main function as migrated so that it doesn't get moved
		# later.
		fun['simplified'] = True
		
		return ast.Module([fun], strings)
	
	elif isinstance(node, oast.Mul):
		left  = translate(node.left,  st, strings, funcName)
		right = translate(node.right, st, strings, funcName)
		
		return ast.Mul(left, right)
	
	elif isinstance(node, oast.Name):
		ret = 'input_int' if node.name == 'input' else node.name
		
		if ret == 'input_int':
			ret = st.getBIF(ret)
		
		else:
			if ret == 'True':
				ret = ast.Tru()
			
			elif ret == 'False':
				ret = ast.Fals()
			
			else:
				ret = st.getSymbol(ret)
		
		return ret
	
	elif isinstance(node, oast.Not):
		operand = translate(node.expr, st, strings, funcName)
		
		return ast.Not(operand)
	
	elif isinstance(node, oast.Or):
		left  = translate(node.nodes[0], st, strings, funcName)
		right = translate(node.nodes[1], st, strings, funcName)
		
		return ast.Or(left, right)
		
	elif isinstance(node, oast.Printnl):
		children = [translate(e, st, strings, funcName) for e in node.getChildNodes()]
		children = util.flatten(children)
		
		return ast.FunctionCall(st.getBIF('print_any'), *children)
	
	elif isinstance(node, oast.Return):
		return ast.Return(translate(node.value, st, strings, funcName))
		
	elif isinstance(node, oast.Stmt):
		stmts = [translate(s, st, strings, funcName) for s in node.getChildNodes()]
		
		return util.flatten(stmts)
	
	elif isinstance(node, oast.Sub):
		left  = translate(node.left,  st, strings, funcName)
		right = translate(node.right, st, strings, funcName)
		
		return ast.Sub(left, right)
	
	elif isinstance(node, oast.Subscript):
		sym = translate(node.expr, st, strings, funcName)
		sub = translate(node.subs[0], st, strings, funcName)
		
		return ast.Subscript(sym, sub)
	
	elif isinstance(node, oast.While):
		cond = translate(node.test, st, strings, funcName)
		
		body = translate(node.body, st, strings, funcName)
		body = ast.BasicBlock(body)
		
		return ast.While(cond, body, st)
	
	elif isinstance(node, oast.UnarySub):
		operand = translate(node.expr, st, strings, funcName)
		
		return ast.Negate(operand)
	
	else:
		raise Exception("Unsupported AST node encountered: {}".format(node.__class__.__name__))
