"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/08/26
Description:	Functions and data structures for allocating registers in x86.
"""

from assembler.registers import Register

class RegisterFile(object):
	def __init__(self):
		self.allocated = []
		self.available = ["eax", "ebx", "ecx", "edx"]

	def alloc(self, name = None):
		if name:
			if name in self.allocated:
				raise Exception("That register (%{0}) is currently allocated".format(name))
			else:
				self.available.remove(name)
				self.allocated.append(name)
				
				return Register(name)
		else:
			if not self.allInUse():
				reg = self.available.pop(0)
				self.allocated.append(reg)
				
				return Register(reg)
			else:
				raise Exception("All registers are currently allocated.")

	def allInUse(self):
		return len(self.available) == 0
	
	def inUse(self, reg):
		return reg in self.allocated

	def free(self, reg):
		if reg.name in self.allocated:
			self.allocated.remove(reg.name)
			
			self.available.append(reg.name)
			self.available.sort()
		else:
			raise Exception("Attempting to free an un-allocated register: {0}".format(reg))
