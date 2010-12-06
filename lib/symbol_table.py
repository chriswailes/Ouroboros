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
	
	def getBIF(self, name):
		return self.getSingleton(Name, name, -1)
	
	def getName(self, name, define = False):
		key = (Name, name)
		
		if self.writeCounters.has_key(key):
			if define:
				next = self.writeCounters[key] + 1
				
				self.setVersion(key, next)
		
		else:
			self.setVersion(key, 0)
		
		return self.getSingleton(Name, name, self.readCounters[key])
	
	def getSingleton(self, typ, name, version):
		trip = (typ, name, version)
		
		if self.singletons.has_key(trip):
			ret = self.singletons[trip]
		else:
			ret = typ(name, version)
			self.singletons[trip] = ret
		
		return ret
	
	def getSymbol(self, name, assign = False):
		key = (Symbol, nam)
		readBeforeWrite = False
		
		if self.writeCounters.has_key(key):
			if assign:
				next = self.writeCounters[key] + 1
				self.setVersion(key, next)
		
		else:
			self.setVersion(key, 0)
			readBeforeWrite = not assign
		
		ret = self.getSingleton(Symbol, name, self.readCounters[key])
		ret['rbw'] = readBeforeWrite
		
		return ret
	
	def getTemp(self):
		tmpName = "!{0}".format(self.tmpCounter)
		self.tmpCounter += 1
		
		return self.getSymbol(tmpName, True)
	
	def rollback(self):
		self.readCounters = self.readSnapshots.pop()
	
	def setVersion(key, version):
		self.readCounters[key] = self.writeCounters[key] = version
	
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
