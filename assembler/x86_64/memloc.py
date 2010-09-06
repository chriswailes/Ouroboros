"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/09/04
Description:	Objects and code for representing memory locations in x86_64.
"""

from assembler import memloc

class Stack(memloc.Stack):
	def __init__(self):
		super(Stack, self).__init__(8)
		
		#Because the stack grows top-down, and we are storing in relation to
		#the stack pointer (and not the base pointer) we need to start at 8
		#bytes above the stack pointer.
		self.size = 8
	
	def newLoc(self, offset, name):
		return Mem(offset, name)

class Mem(memloc.Mem):
	def __str__(self):
		return "{0:d}(%rsp)".format(self.offset)
