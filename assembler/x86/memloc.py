"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/09/02
Description:	Objects and code for representing memory locations in x86.
"""

from assembler import memloc

class Stack(memloc.Stack):
	def __init__(self):
		super(Stack, self).__init__(4)
	
	def newLoc(self, offset, name):
		return Mem(offset, name)

class Mem(memloc.Mem):
	def __str__(self):
		return "-{0:d}(%ebp)".format(self.offset)
