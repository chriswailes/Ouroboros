"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/08/27
Description:	Removes redundant move operations from the generated assembly
			code.
"""

import ib

def redundantMoves(code):
	while (not code.atEnd()):
		cur = code.getCurInst()
		
		if cur.name == "mov":
			index = code.pos + 1
			ahead = code.getInst(index)
			
			while ahead:
				if cur.src == "%eax" and (ahead.name == "mul" or ahead.name == "imul"):
					break
				elif cur.src == "%eax" and (ahead.name == "div" or ahead.name == "idiv"):
					break
				elif cur.src == "%eax" and ahead.name == "call":
					break
				elif isinstance(ahead, ib.OneOp) and cur.src == ahead.dest:
					break
				elif isinstance(ahead, ib.TwoOp) and cur.src == ahead.dest and ahead.src != cur.dest:
					break
				elif ahead.name == "mov" and cur.dest == ahead.src and cur.src == ahead.dest:
					code.removeInst(index)
				
				index += 1
				ahead = code.getInst(index)
		
		code.next()
