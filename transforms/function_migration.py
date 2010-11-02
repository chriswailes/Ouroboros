"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/10/21
Description:	A transformation that moves function definitions out of the body
			of a module and into the module's functions variable.
"""

from lib.ast import *
from lib import util

analysis	= []
args		= []

def init():
	from transforms.pass_manager import register
	register('function_migration', migrateFunctions, analysis, args)

def migrateFunctions(node, st = None, funs = []):
	newChildren = []
	
	if isinstance(node, Module):
		funs = []
	
	st = node.st if isinstance(node, BasicBlock) else st
	
	for child in node:
		if isinstance(child, Function):
			funs.append(child)
			migrateFunctions(child, st, funs)
		
		else:
			migrateFunctions(child, st, funs)
			newChildren.append(child)
	
	node.setChildren(newChildren)
	
	if isinstance(node, Module):
		node.functions = funs
