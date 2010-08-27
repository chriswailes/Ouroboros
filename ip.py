"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/08/27
Description:	Classes and functions for doing instruction optimization passes.
"""

import sys

import ib

def doInstructionPasses(code):
	code.reset()
	
	#printPass(code)
	redundantMoves(code)

def redundantMoves(code):
	while (not code.atEnd()):
		cur = code.getCurInst()
		next = code.getNextInst()
		
		if next != None:
			if (cur.name == "mov") and (next.name == "mov") and (cur.dest == next.src):
				code.removeNextInst()
		
		code.next()

def printPass(code):
	while (not code.atEnd()):
		sys.stdout.write(str(code.getCurInst()))
		code.next()
