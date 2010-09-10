"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/09/03
Description:	Classes and functions for building x86_64 instructions.
"""

from assembler import ib
from assembler.ib import Block, Immediate, Instruction, Labeler, Label

from assembler.x86_64.memloc import Mem

class OneOp(ib.OneOp):
	def __init__(self, name, dest = None, suffix = "q", comment = ""):
		if isinstance(dest, Mem):
			comment = comment or "Var: " + dest.name
		
		super(OneOp, self).__init__(name, dest, suffix, comment)

class TwoOp(ib.TwoOp):
	def __init__(self, name, src = None, dest = None, suffix = "q", comment = ""):
		if isinstance(src, Mem) and isinstance(dest, Mem):
			raise Exception("Both operands are memory locations.")
		elif isinstance(src, Mem):
			comment = comment or "Var: " + src.name
		elif isinstance(dest, Mem):
			comment = comment or "Var: " + dest.name
		
		super(TwoOp, self).__init__(name, src, dest, suffix, comment)
