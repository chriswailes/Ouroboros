"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/08/26
Description:	The symbol table used by Pycom.
"""

from lib.ast import *

class SymbolTable(object):
	def __init__(self, other = None):
		if other:
			self.symbols = other.symbols.copy()
			self.names = other.names.copy()
			self.singletons = other.singletons.copy()
			self.strings = other.strings.copy()
		else:
			self.symbols = {}
			self.names = {}
			self.singletons = {}
			self.strings = {}
	
	def __str__(self):
		return "SymbolTable #{0}".format(id(self))
	
	def getName(self, name, bif = True, define = False):
		#Left value  -> next assignment
		#Right value -> current read
		
		if bif:
			return self.getSingleton(name, -1, Name)
		
		else:
			if self.names.has_key(name):
				if define:
					a, _ = self.names[name]
					self.names[name] = (a + 1, a + 1)
			
			else:
				self.names[name] = (0, 0)
			
			_, b = self.names[name]
			return self.getSingleton(name, b, Name)
	
	def getSingleton(self, name, version, typ = Symbol):
		trip = (typ, name, version)
		ret = None
		
		if self.singletons.has_key(trip):
			ret = self.singletons[trip]
		else:
			ret = Symbol(name, version) if typ == Symbol else Name(name, version)
			self.singletons[trip] = ret
		
		return ret
	
	#~def getStrings(self, string):
		#~if not self.strings.has_key(string):
			#~self.strings[string] = String(string)
		#~
		#~return self.strings[string]
	
	def getSymbol(self, name = '!', assign = False):
		#Left value  -> next assignment
		#Right value -> current read
		
		readBeforeWrite = False
		
		if self.symbols.has_key(name):
			if assign:
				a, _ = self.symbols[name]
				self.symbols[name] = (a + 1, a + 1)
		else:
			self.symbols[name] = (0, 0)
			
			readBeforeWrite = not assign
		
		_, b = self.symbols[name]
		ret = self.getSingleton(name, b)
		ret['rbw'] = readBeforeWrite
		
		return ret
	
	def update(self, other):
		if isinstance(other, SymbolTable):
			for pair in other.symbols:
				if self.symbols.has_key(pair):
					_, b0 = self.symbols[pair]
					a1, _ = other.symbols[pair]
					
					self.symbols[pair] = (a1, b0)
			
			for trip in other.singletons:
				singleton = other.singletons[trip]
				
				if isinstance(singleton, Name) or singleton['rbw']:
					self.singletons[trip] = singleton
		
		elif isinstance(other, Join):
			for phi in other.phis:
				if self.symbols.has_key(phi.target.name):
					a0, _ = self.symbols[phi.target.name]
					b1 = phi.target.version
					
					pair = (phi.target.name, b1)
					self.symbols[phi.target.name] = (a0, b1)
					
					trip = (Symbol, phi.target.name, b1)
					self.singletons[trip] = phi.target
