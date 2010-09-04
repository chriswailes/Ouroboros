"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/09/02
Description:	Objects and code for representing memory locations.
"""

class Stack(object):
	def __init__(self):
		self.size = 0
		self.addrs = {}
	
	def getAddr(self, var):
		if not self.addrs.has_key(var):
			self.addrs[var] = self.size
			self.size += self.wordSize
		
		return self.addrs[var]
