"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/11/05
Description:	A transformation that moves strings up to the Module level.
"""

from lib.ast import *
from lib import util

from lib.symbol_table import SymbolTable

analysis	= []
args		= ['cf']

def init():
	from transforms.pass_manager import register
	register('strings', ripStrings, analysis, args)

def ripStrings(node, cf, st = None, strings = {}, inClassBody = False):
	if isinstance(node, Module):
		strings = {}
	
	elif isinstance(node, Function):
		st = node.st
	
	elif isinstance(node, Class):
		inClassBody = True
	
	elif isinstance(node, GetAttr):
		string = node.attrName.name
		
		if not strings.has_key(string):
			sym = st.getSymbol(assign = True)
			sym['color'] = cf.getDataLabel()
			sym['color'].reference = True
			sym['scope'] = 'global'
		
			strings[string] = sym
		
		else:
			sym = strings[string]
		
		node.attrName = sym
	
	elif isinstance(node, Assign) and inClassBody:
		sym = node.var
		string = sym.name
		
		if not strings.has_key(string):
			sym['color'] = cf.getDataLabel()
			sym['color'].reference = True
			sym['scope'] = 'global'
			
			strings[string] = sym
		
		else:
			node.var = strings[string]
	
	for child in node:
		ripStrings(child, cf, st, strings, inClassBody)
	
	if isinstance(node, Module):
		node.strings = strings
