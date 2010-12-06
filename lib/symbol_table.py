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
			self.singletons	= other.singletons.copy()
			self.tmpCounter	= other.tmpCounter
			
			self.readCounters	= other.readCounters.copy()
			self.readSnapshots	= list(other.readSnapshots)
			self.writeCounters	= other.writeCounters.copy()
		
		else:
			self.singletons	= {}
			self.tmpCounter	= 0
			
			self.readCounters	= {}
			self.readSnapshots	= []
			self.writeCounters	= {}
	
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
			ret = typ(name, version)
			self.singletons[trip] = ret
		
		return ret
	
	def getSymbol(self, name, assign = False):
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
	
	def getTemp(self):
		tmpName = "!{0}".format(self.tmpCounter)
		self.tmpCounter += 1
		
		return self.getSymbol(tmpName, True)
	
	def rollback(self):
		self.readCounters = self.readSnapshots.pop()
	
	def snapshot(self):
		self.readSnapshots.append(self.readCounters)
	
	#This is here to deal with read-before-write symbols in functions.
	def update(self, other):
		if isinstance(other, SymbolTable):
			
			#Update the temp counter so that we only get one instance of a
			#temporary variable number throughout the entire program.
			self.tmpCounter = other.tmpCounter
			
			for trip in other.singletons:
				singleton = other.singletons[trip]
				
				if isinstance(singleton, Name) or singleton['rbw']:
					self.singletons[trip] = singleton
		
		else:
			raise Exception("Trying to update a SymbolTable with something that isn't a SymbolTable")
