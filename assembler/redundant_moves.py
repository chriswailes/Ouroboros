"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		Ouroboros
Date:		2010/08/27
Description:	Removes redundant move operations from the generated assembly
			code.
"""

from lib.config import config

import ib

def redundantMoves(code):
	if config.arch == 'x86':
		from x86 import redundant_moves as arch
	elif config.arch == 'x86_64':
		from x86_64 import redundant_moves as arch
	else:
		raise Exception("Unknown architecture.")
	
	return arch.redundantMoves(code)
