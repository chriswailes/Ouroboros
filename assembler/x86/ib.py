"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/08/26
Description:	Classes and functions for building x86 instructions.
"""

from assembler import ib
from assembler.ib import Block, Immediate, Instruction, Labeler, Label

from assembler.coloring import Mem

class OneOp(ib.OneOp):
	def __init__(self, name, operand = None, suffix = "l", comment = ""):
		super(OneOp, self).__init__(name, operand, suffix, comment)

class TwoOp(ib.TwoOp):
	def __init__(self, name, src = None, dest = None, suffix = "l", comment = ""):
		if isinstance(src, Mem) and isinstance(dest, Mem):
			raise Exception("Both operands are memory locations.")
		
		super(TwoOp, self).__init__(name, src, dest, suffix, comment)
