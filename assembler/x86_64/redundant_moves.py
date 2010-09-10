"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/09/06
Description:	Removes redundant move operations from the generated x86_64
			assembly code.
"""

from assembler.x86_64 import ib

from assembler.x86_64.memloc import Mem
from assembler.x86_64.registers import Register

def redundantMoves(code):
	while (not code.atEnd()):
		cur = code.getCurInst()
		
		if cur.name == 'mov':
			index = code.pos + 1
			ahead = code.getInst(index)
			
			while ahead:
				if cur.name[0] == 'j':
					break
				elif cur.src == Register('rax') and (ahead.name == 'mul' or ahead.name == 'imul'):
					break
				elif cur.src == Register('rax') and (ahead.name == 'div' or ahead.name == 'idiv'):
					break
				elif cur.src == Register('rax') and ahead.name == 'call':
					break
				elif isinstance(ahead, ib.OneOp) and cur.src == ahead.dest:
					break
				elif isinstance(ahead, ib.TwoOp) and cur.src == ahead.dest:
					if ahead.src != cur.dest:
						break
					elif ahead.name == 'mov':
						code.removeInst(index)
				
				index += 1
				ahead = code.getInst(index)
		
		code.next()
