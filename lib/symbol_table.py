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
	
	def getSymbol(self, name = '!', assign = False):
		if self.symbols.has_key(name):
			if assign:
				a, _ = self.symbols[name]
				self.symbols[name] = (a + 1, a + 1)
		else:
			self.symbols[name] = (0, 0)
		
		_, b = self.symbols[name]
		return Symbol(name, b)
	
	def update(self, other):
		for s in other.symbols:
			if self.symbols.has_key(s):
				_, b0 = self.symbols[s]
				a1, _ = other.symbols[s]
				
				self.symbols[s] = (a1, b0)

class Symbol(object):
	def __init__(self, name, version):
		self.name = name
		self.version = version
	
	def __eq__(self, other):
		return self.name == other.name and self.version == other.version
	
	def __str__(self):
		return "{0}:{1:d}".format(self.name, self.version)
