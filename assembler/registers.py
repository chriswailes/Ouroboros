"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/08/26
Description:	Functions and data structures for allocating abstract registers.
"""

class Register(object):
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
