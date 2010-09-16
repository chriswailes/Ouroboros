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

from variables import VFile

def translate(node, v = None, funcName = False):
	if isinstance(node, oast.Add):
		left = translate(node.left, v)
		right = translate(node.right, v)
		
		return ast.Add(left, right)
	
	elif isinstance(node, oast.Assign):
		#Translate the right hand side first so it can use the older version
		#of the left hand side.
		expr = translate(node.expr, v)
		name = translate(node.nodes.pop(), v)
		
		return ast.Assign(name, expr)
	
	elif isinstance(node, oast.AssName):
		name = v.getVar(node.name, True)
		return ast.Name(name)
		
		#name = v.userVar(node.name)
		#return ast.Name(name)
	
	elif isinstance(node, oast.CallFunc):
		name = translate(node.node, v, True)
		args = [translate for a in node.args]
		
		return ast.FunctionCall(name, args)
	
	elif isinstance(node, oast.Const):
		return ast.Integer(node.value)
	
	elif isinstance(node, oast.Discard):
		return translate(node.expr, v)
	
	elif isinstance(node, oast.Div):
		left = translate(node.left, v)
		right = translate(node.right, v)
		
		return ast.Div(left, right)
	
	elif isinstance(node, oast.If):
		tests = node.tests
		cond, then = tests.pop(0)
		
		cond = translate(cond, v)
		
		#A new VFile needs to be constructed for the then branch.
		vThen = VFile(v.variables)
		then = ast.BasicBlock(translate(then, vThen), vThen)
		
		els = None
		
		#A new VFile needs to be constructed for the else branch.
		vElse = VFile(v.variables)
		
		if len(tests) > 0:
			els = [translate(oast.If(tests, node.else_), vElse)]
		else:
			els = translate(node.else_, vElse)
		
		els = ast.BasicBlock(els, vElse)
		
		return ast.If(cond, then, els)
		
	elif isinstance(node, oast.Module):
		#Create a new VFile for this module.
		v = VFile()
		children = ast.BasicBlock(translate(node.node, v), v)
		
		return ast.Module(children)
	
	elif isinstance(node, oast.Mul):
		left = translate(node.left, v)
		right = translate(node.right, v)
		
		return ast.Mul(left, right)
	
	elif isinstance(node, oast.Name):
		name = node.name
		if not funcName:
			name = v.getVar(name)
		
		return ast.Name(name)
		
	elif isinstance(node, oast.Printnl):
		children = util.flatten([translate(e, v) for e in node.getChildNodes()])
		
		return ast.FunctionCall(ast.Name("print_int_nl"), children)
		
	elif isinstance(node, oast.Stmt):
		stmts = [translate(s, v) for s in node.getChildNodes()]
		
		return util.flatten(stmts)
	
	elif isinstance(node, oast.Sub):
		left = translate(node.left, v)
		right = translate(node.right, v)
		
		return ast.Sub(left, right)
		
	elif isinstance(node, oast.UnarySub):
		operand = translate(node.expr, v)
		
		return ast.Negate(operand)
	
	else:
		None
