"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/09/20
Description:	The __init__.py file for the assembler module.
"""

class Spill(Exception):
	def __init__(self, symbols):
		self.symbols = symbols
	
	def __str__(self):
		"Spill: {0}".format(self.symbols)
