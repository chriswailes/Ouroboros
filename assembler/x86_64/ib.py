"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/08/26
Description:	Classes and functions for building x86_64 instructions.
"""

from assembler import ib
from assembler.ib import Block, Instruction

class OneOp(ib.OneOp):
	def __init__(self, name, dest = None, suffix = "q", comment = ""):
		super(OneOp, self).__init__(name, dest, suffix, comment)

class TwoOp(ib.TwoOp):
	def __init__(self, name, src = None, dest = None, suffix = "q", comment = ""):
		super(TwoOp, self).__init__(name, src, dest, suffix, comment)
