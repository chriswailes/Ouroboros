"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/08/26
Description:	The symbol table used by Pycom.
"""

from lib.ast import *

singletons = {}

def getSingleton(name, version, typ = Symbol):
	global singletons
	
	pair = (name, version)
	sym = None
	
	if singletons.has_key(pair):
		sym = singletons[pair]
	else:
		sym = Symbol(name, version) if typ == Symbol else Name(name)
		singletons[pair] = sym
	
	return sym

class SymbolTable(object):
	def __init__(self, other = None):
		if other:
			self.symbols = other.symbols.copy()
		else:
			self.symbols = {}
	
	def getName(self, name):
		return getSingleton(name, 0, Name)
	
	def getSymbol(self, name = '!', assign = False):
		#Left value  -> next assignment
		#Right value -> current read
		
		if self.symbols.has_key(name):
			if assign:
				a, _ = self.symbols[name]
				self.symbols[name] = (a + 1, a + 1)
		else:
			self.symbols[name] = (0, 0)
		
		_, b = self.symbols[name]
		return getSingleton(name, b)
	
	def update(self, other):
		if isinstance(other, SymbolTable):
			for s in other.symbols:
				if self.symbols.has_key(s):
					_, b0 = self.symbols[s]
					a1, _ = other.symbols[s]
					
					self.symbols[s] = (a1, b0)
		
		elif isinstance(other, ast.Join):
			for phi in other.phis:
				if self.symbols.has_key(phi.target.symbol.name):
					a0, _ = self.symbols[phi.target.symbol.name]
					b1 = phi.target.symbol.version
					
					pair = (phi.target.symbol.name, b1)
					
					self.symbols[phi.target.symbol.name] = (a0, b1)
