"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/09/20
Description:	x86 specific coloring code and data structures.
"""

#sc stands for SuperColoring
from assembler import coloring as sc

colorStrings = ['eax', 'ebx', 'ecx', 'edx', 'esi', 'edi']

colors = [sc.Register(r) for r in colorStrings]

class ColorFactory(sc.ColorFactory):
	def __init__(self):
		super(sc.ColorFactory, self).__init__(4)
	
	def newColor(self, offset, name):
		return Mem(offset, name)

class Mem(sc.Mem):
	def __str__(self):
		return "-{0:d}(%ebp)".format(self.offset)

def precolor(tree):
	pass
