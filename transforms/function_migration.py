"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		Ouroboros
Date:		2010/10/21
Description:	A transformation that moves function definitions out of the body
			of a module and into the module's functions variable.
"""

from lib.ast import *

analysis	= []
args		= []

def init():
	from transforms.pass_manager import register
	register('function_migration', migrateFunctions, analysis, args)

def migrateFunctions(node, st = None, funs = None):
	newChildren	= []
	funs			= [] if isinstance(node, Module) else funs
	st			= node.st if isinstance(node, Function) else st
	
	for child in node:
		migrateFunctions(child, st, funs)
		
		if isinstance(child, Function):
			funs.append(child)
		
		else:
			newChildren.append(child)
	
	node.setChildren(newChildren)
	
	if isinstance(node, Module):
		node.functions = funs
