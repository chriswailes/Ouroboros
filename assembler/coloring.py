"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/09/20
Description:	Generic assembler coloring classes and functions.
"""

from lib.config import config

def getColorFactory():
	if config.arch == 'x86':
		from x86.coloring import ColorFactory as CF
	elif config.arch == 'x86_64':
		from x86_64.coloring import ColorFactory as CF
	
	return CF()

def precolor(tree):
	if config.arch == 'x86':
		from x86.coloring import precolor
	elif config.arch == 'x86_64':
		from x86_64.coloring import precolor
	
	precolor(tree)

def interfere(tree, ig):
	if config.arch == 'x86':
		from x86.coloring import interfere
	elif config.arch == 'x86_64':
		from x86_64.coloring import interfere
	
	interfere(tree, ig)

class ColorFactory(object):
	def __init__(self, wordSize, startingColors):
		self.offset = 0
		self.startingColors = startingColors
		self.wordSize = wordSize
	
	def newColor(self, symbol = None):
		color = None
		
		if len(self.startingColors) > 0:
			color = self.startingColors.pop(0)
		else:
			color = self.makeColor(symbol)
			self.offset += self.wordSize
		
		return color

class Color(object):
	pass

class Mem(Color):
	def __init__(self, offset, name):
		self.offset = offset
		self.name = name
	
	def __eq__(self, other):
		if isinstance(other, Mem):
			return self.offset == other.offset
		else:
			return False
	
	def __ne__(self, other):
		if isinstance(other, Mem):
			return self.offset != other.offset
		else:
			return True

class Register(Color):
	def __init__(self, name, symbol = None):
		self.name = name
		self.symbol = symbol
	
	def __eq__(self, other):
		if isinstance(other, Register):
			return self.name == other.name
		else:
			return False
	
	def __ne__(self, other):
		if isinstance(other, Register):
			return self.name != other.name
		else:
			return True
	
	def __str__(self):
		return '%' + self.name
