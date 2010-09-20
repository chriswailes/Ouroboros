"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/09/20
Description:	x86 specific coloring code and data structures.
"""

from assembler.coloring import Register
from assembler.coloring import ColorFactory as SuperColorFactory
from assembler.coloring import Mem as SuperMem

from lib.ast import *
from lib.symbol_table import Symbol

colorStrings = ['eax', 'ebx', 'ecx', 'edx', 'esi', 'edi']
colors = [Register(r) for r in colorStrings]

#Symbols used for cause interference across function cals.
alex = Symbol('alex', -1)
alex['color'] = Register('eax')

chuck = Symbol('chuck', -1)
chuck['color'] = Register('ecx')

dave = Symbol('dave', -1)
dave['color'] = Register('edx')

jerks = set([alex, chuck, dave])

class ColorFactory(SuperColorFactory):
	def __init__(self):
		super(ColorFactory, self).__init__(4, colors)
	
	def makeColor(self, symbol = None):
		return Mem(self.offset, symbol)

class Mem(SuperMem):
	def __str__(self):
		return "-{0:d}(%ebp)".format(self.offset)

def interfere(node, ig):
	#Alex, Chuck, and Dave will be doing our interfering today.
	global jerks
	
	if isinstance(node, FunctionCall):
		for sym in node['pre-alive']:
			ig[sym] = ig[sym] | jerks
	
	for child in node:
		interfere(child, ig)

def precolor(tree):
	pass
