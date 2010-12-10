"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		Ouroboros
Date:		2010/09/06
Description:	Removes redundant move operations from the generated x86_64
			assembly code.
"""

from assembler.x86_64 import ib

from assembler.coloring import Mem, Register

def redundantMoves(code):
	while (not code.atEnd()):
		cur = code.getCurInst()
		
		if cur.name == 'mov':
			index = code.pos + 1
			
			if cur.src == cur.dest:
				code.removeInst(code.pos)
			
			else:
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
					elif isinstance(ahead, ib.OneOp) and cur.src == ahead.operand:
						break
					elif isinstance(ahead, ib.TwoOp) and cur.src == ahead.dest:
						if ahead.src != cur.dest:
							break
						elif ahead.name == 'mov':
							code.removeInst(index)
				
					index += 1
					ahead = code.getInst(index)
		
		code.next()
