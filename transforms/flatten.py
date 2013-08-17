"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		Ouroboros
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
	newInPlace	= None
	preStmts		= []
	
	# Setup flattening for this node's children.
	if util.classGuard(node, Assign, BasicBlock, Module):
		newInPlace = node.__class__
	
	elif isinstance(node, Function):
		st = node.st
	
	# Flatten our children.
	if isinstance(node, While):
		if not isinstance(node.cond, Symbol):
			condBody, node.cond = flatten(node.cond, st)
			node.condBody = BasicBlock(condBody)
		
		bodyPreStmts, node.body = flatten(node.body, st)
		preStmts.append(bodyPreStmts)
	
	elif isinstance(node, If):
		for child in node:
			childPreStmts, newChild = flatten(child, st, newInPlace)
			
			preStmts.append(childPreStmts)
			newChildren.append(newChild)
		
		# Set our new child nodes.
		newChildren = util.flatten(newChildren)
		node.setChildren(newChildren)
	
	else:
		for child in node:
			childPreStmts, newChild = flatten(child, st, newInPlace)
			
			if isinstance(node, BasicBlock):
				newChildren.append(childPreStmts)
				newChildren.append(newChild)
			
			else:
				preStmts.append(childPreStmts)
				newChildren.append(newChild)
		
		# Set our new child nodes.
		newChildren = util.flatten(newChildren)
		node.setChildren(newChildren)
	
	# Flatten the current node.
	if classGuard(node, BinOp, FunctionCall, IfExp, UnaryOp) and not inPlace:
		sym = st.getTemp()
		preStmts.append(Assign(sym, node))
		
		node = sym
	
	# Flatten our list of pre-statements.
	preStmts = util.flatten(preStmts)
	
	return node if isinstance(node, Module) else (preStmts, node)
