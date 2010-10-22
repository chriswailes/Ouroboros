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
	
	trip = (typ, name, version)
	ret = None
	
	if singletons.has_key(trip):
		ret = singletons[trip]
	else:
		ret = Symbol(name, version) if typ == Symbol else Name(name, version)
		singletons[trip] = ret
	
	return ret

class SymbolTable(object):
	def __init__(self, other = None):
		if other:
			self.symbols = other.symbols.copy()
			self.names = other.names.copy()
		else:
			self.symbols = {}
			self.names = {}
	
	def getName(self, name, bif = True, define = False):
		#Left value  -> next assignment
		#Right value -> current read
		
		if bif:
			return getSingleton(name, -1, Name)
		
		else:
			if self.names.has_key(name):
				if define:
					a, _ = self.names[name]
					self.names[name] = (a + 1, a + 1)
			
			else:
				self.names[name] = (0, 0)
			
			_, b = self.names[name]
			return getSingleton(name, b, Name)
	
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
		
		elif isinstance(other, Join):
			for phi in other.phis:
				if self.symbols.has_key(phi.target.name):
					a0, _ = self.symbols[phi.target.name]
					b1 = phi.target.version
					
					pair = (phi.target.name, b1)
					
					self.symbols[phi.target.name] = (a0, b1)
