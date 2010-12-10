"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		Ouroboros
Date:		2010/09/20
Description:	The __init__.py file for the assembler module.
"""

class Spill(Exception):
	def __init__(self, syms):
		self.symbols = set(syms)
	
	def __str__(self):
		"Spill: {0}".format(self.symbols)
