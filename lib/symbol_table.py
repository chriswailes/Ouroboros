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
			self.singletons = other.singletons.copy()
			self.funSymbols = list(other.funSymbols)
		else:
			self.symbols = {}
			self.singletons = {}
			self.funSymbols = []
	
	def getSingleton(self, name, version):
		pair = (name, version)
		sym0 = None
		
		if self.singletons.has_key(pair):
			sym0 = self.singletons[pair]
		else:
			sym0 = Symbol(name, version)
			self.singletons[pair] = sym0
		
		return sym0
	
	def getFunSymbol(self, name):
		sym0 = None
		
		for sym1 in self.funSymbols:
			if sym1.name == name:
				sym0 = sym1
				break
		
		if not sym0:
			sym0 = FunSymbol(name)
			self.funSymbols.append(sym0)
		
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
					
			self.singletons.update(other.singletons)
		
		elif isinstance(other, ast.Join):
			for phi in other.phis:
				if self.symbols.has_key(phi.target.symbol.name):
					a0, _ = self.symbols[phi.target.symbol.name]
					b1 = phi.target.symbol.version
					
					pair = (phi.target.symbol.name, b1)
					self.singletons[pair] = phi.target.symbol
					
					self.symbols[phi.target.symbol.name] = (a0, b1)

class FunSymbol(dict):
	def __init__(self, name):
		self.name = name
	
	def __eq__(self, other):
		if isinstance(other, FunSymbol):
			return self.name == other.name
		else:
			return False
	
	def __hash__(self):
		return hash(str(self))
	
	def __ne__(self, other):
		if isinstance(other, FunSymbol):
			return self.name != other.name
		else:
			return True
	
	def __repr__(self):
		return str(self)
	
	def __str__(self):
		return self.name

class Symbol(dict):
	def __init__(self, name, version):
		self.name = name
		self.version = version
	
	def __eq__(self, other):
		if isinstance(other, Symbol):
			return self.name == other.name and self.version == other.version
		else:
			return False
	
	def __hash__(self):
		return hash(str(self))
	
	def __ne__(self, other):
		if isinstance(other, Symbol):
			return self.name != other.name or self.version != other.version
		else:
			return True
	
	def __repr__(self):
		return str(self)
	
	def __str__(self):
		return "{0}:{1:d}".format(self.name, self.version)
