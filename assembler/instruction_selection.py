"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/09/02
Description:	The wrapper for our instruction selection code.
"""

from lib.config import config

def selectInstructions(tree, stackSize):
	if config.arch == 'x86':
		from x86 import instruction_selection as arch
	elif config.arch == 'x86_64':
		from x86_64 import instruction_selection as arch
	else:
		raise Exception("Unknown architecture.")
	
	return arch.selectInstructions(tree, stackSize = stackSize)
