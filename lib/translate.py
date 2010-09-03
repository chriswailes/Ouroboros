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
import variables as v

def translate(node, funcName = False):
	if isinstance(node, oast.Add):
		left = translate(node.left)
		right = translate(node.right)
		
		return ast.Add(left, right)
	
	elif isinstance(node, oast.Assign):
		name = translate(node.nodes.pop())
		expr = translate(node.expr)
		
		return ast.Assign(name, expr)
	
	elif isinstance(node, oast.AssName):
		name = v.addUserVar(node.name)
		return ast.Name(name)
	
	elif isinstance(node, oast.CallFunc):
		name = translate(node.node, True)
		args = [translate for a in node.args]
		
		return ast.FunctionCall(name, args)
	
	elif isinstance(node, oast.Const):
		return ast.Integer(node.value)
	
	elif isinstance(node, oast.Discard):
		return translate(node.expr)
	
	elif isinstance(node, oast.Div):
		left = translate(node.left)
		right = translate(node.right)
		
		return ast.Div(left, right)
		
	elif isinstance(node, oast.Module):
		children = util.flatten([translate(n) for n in node.getChildNodes()])
		
		return ast.Module(children)
	
	elif isinstance(node, oast.Mul):
		left = translate(node.left)
		right = translate(node.right)
		
		return ast.Mul(left, right)
	
	elif isinstance(node, oast.Name):
		name = node.name
		if not funcName:
			name = v.addUserVar(node.name)
		
		return ast.Name(name)
		
	elif isinstance(node, oast.Printnl):
		children = util.flatten([translate(e) for e in node.getChildNodes()])
		
		return ast.FunctionCall(ast.Name("print_int_nl"), children)
		
	elif isinstance(node, oast.Stmt):
		stmts = util.flatten([translate(s) for s in node.getChildNodes()])
		
		return stmts
	
	elif isinstance(node, oast.Sub):
		left = translate(node.left)
		right = translate(node.right)
		
		return ast.Sub(left, right)
		
	elif isinstance(node, oast.UnarySub):
		operand = translate(node.expr)
		
		return ast.Negate(operand)
	
	else:
		None
