"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/09/02
Description:	Objects and code for representing memory locations.
"""

class Stack(object):
	def __init__(self, wordSize):
		self.size = 0
		self.addrs = {}
		self.wordSize = wordSize
	
	def getAddr(self, var):
		if isinstance(var, Mem):
			return var
		else:
			if not self.addrs.has_key(var):
				self.addrs[var] = self.size
				self.size += self.wordSize
				
			return self.newLoc(self.addrs[var], var)

class Mem(object):
	def __init__(self, offset, name):
		self.offset = offset
		self.name = name
	
	def __eq__(self, other):
		if isinstance(other, Mem):
			return self.offset == other.offset
		else:
			return False
	
	def __ne__(self, other):
		if isinstance(other, Mem):
			return self.offset != other.offset
		else:
			return True
