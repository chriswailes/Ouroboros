"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		Ouroboros
Date:		2010/08/26
Description:	Classes and functions for building x86 instructions.
"""

from assembler import *
from assembler.coloring import Mem, Register
from assembler.ib import *

class OneOp(ib.OneOp):
	def __init__(self, name, operand = None, suffix = "l", comment = ""):
		super(OneOp, self).__init__(name, operand, suffix, comment)

class TwoOp(ib.TwoOp):
	def __init__(self, name, src = None, dest = None, suffix = "l", comment = ""):
		if isinstance(src, Mem) and isinstance(dest, Mem):
			raise Exception("Both operands are memory locations.")
		
		super(TwoOp, self).__init__(name, src, dest, suffix, comment)
