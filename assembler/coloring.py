"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/09/20
Description:	Generic coloring classes and functions.
"""

class ColorFactory(object):
	def __init__(self, worSize):
		self.size = 0
		self.addrs = {}
		self.wordSize = wordSize

class Color(object):
	pass

class Mem(Color):
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

class Register(Color):
	def __init__(self, name):
		self.name = name
	
	def __eq__(self, other):
		if isinstance(other, Register):
			return self.name == other.name
		else:
			return False
	
	def __ne__(self, other):
		if isinstance(other, Register):
			return self.name != other.name
		else:
			return True
	
	def __str__(self):
		return '%' + self.name
