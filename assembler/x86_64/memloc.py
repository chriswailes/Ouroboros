"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/09/04
Description:	Objects and code for representing memory locations in x86_64.
"""

class Stack(object):
	def __init__(self):
		self.size = 0
		self.addrs = {}
		self.wordSize = 8
	
	def getAddr(self, var):
		if isinstance(var, Mem):
			return var
		else:
			if not self.addrs.has_key(var):
				self.addrs[var] = self.size
				self.size += self.wordSize
				
			return Mem(self.addrs[var], var)

class Mem(object):
	def __init__(self, offset, name):
		self.offset = offset
		self.name = name
	
	def __str__(self):
		return "{0:d}(%rsp)".format(self.offset)
