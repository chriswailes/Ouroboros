"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/08/26
Description:	The symbol table used by Pycom.
"""

import ast

class SymbolTable(object):
	def __init__(self, other = None):
		if other:
			self.symbols = other.symbols.copy()
		else:
			self.symbols = {}
		
		self.singletons = []
	
	def getSingleton(self, name, version):
		sym0 = None
		
		for sym1 in self.singletons:
			if sym1.name == name and sym1.version == version:
				sym0 = sym1
				break
		
		if not sym0:
			sym0 = Symbol(name, version)
			self.singletons.append(sym0)
		
		return sym0
	
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
		return self.getSingleton(name, b)
	
	def update(self, other):
		if isinstance(other, SymbolTable):
			for s in other.symbols:
				if self.symbols.has_key(s):
					_, b0 = self.symbols[s]
					a1, _ = other.symbols[s]
					
					self.symbols[s] = (a1, b0)
		
		elif isinstance(other, ast.Join):
			for phi in other.phis:
				if self.symbols.has_key(phi.target.name):
					a0, _ = self.symbols[phi.target.name]
					b1 = phi.target.version
					
					self.symbols[phi.target.name] = (a0, b1)

class Symbol(object):
	def __init__(self, name, version):
		self.color = None
		self.name = name
		self.version = version
	
	def __eq__(self, other):
		return self.name == other.name and self.version == other.version
	
	def __ne__(self, other):
		return self.name != other.name or self.version != other.version
	
	def __repr__(self):
		return str(self)
	
	def __str__(self):
		return "{0}:{1:d}".format(self.name, self.version)
