"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/09/20
Description:	Generic assembler coloring classes and functions.
"""

from lib.config import config

def precolor(tree, ig):
	if config.arch == 'x86':
		from x86.coloring import precolor
	elif config.arch == 'x86_64':
		from x86_64.coloring import precolor
	
	precolor(tree, ig)

class ColorFactory(object):
	def __init__(self):
		self.offset = 0
		
		if config.arch == 'x86':
			from x86.coloring import wordSize, colors
		elif config.arch == 'x86_64':
			from x86_64.coloring import wordSize, colors
		
		self.colors = set(colors)
		self.wordSize = wordSize
	
	def getColor(self, interference = set([]), test = None):
		color = None
		
		allocated = []
			
		for sym in interference:
			if sym.has_key('color'):
				allocated.append(sym['color'])
		
		allocated = set(allocated)
		free = self.colors - allocated
		
		if test != None:
			filteredFree = []
			
			for color in free:
				if isinstance(color, test):
					filteredFree.append(free)
			
			free = filteredFree
		
		else:
			free = list(free)
		
		if len(free) > 0:
			free.sort()
			color = free[0]
		
		elif test != Register:
			color = Mem(self.offset)
			self.offset += self.wordSize
			
			self.colors = self.colors | set([color])
		
		return color

class Color(object):
	def __repr__(self):
		return str(self)

class Mem(Color):
	def __init__(self, offset):
		self.offset = offset
		
		if config.arch == 'x86':
			from x86.coloring import memFormatString
		elif config.arch == 'x86_64':
			from x86_64.coloring import memFormatString
		
		self.formatString = memFormatString
	
	def __eq__(self, other):
		if isinstance(other, Mem):
			return self.offset == other.offset
		else:
			return False
	
	def __ge__(self, other):
		if isinstance(other, Register):
			return True
		
		elif isinstance(other, Mem):
			return self.offset >= other.offset
		
		else:
			return False
	
	def __gt__(self, other):
		if isinstance(other, Register):
			return True
		
		elif isinstance(other, Mem):
			return self.offset > other.offset
		
		else:
			return False
	
	def __lt__(self, other):
		if isinstance(other, Register):
			return False
		
		elif isinstance(other, Mem):
			return self.offset < other.offset
		
		else:
			return False
	
	def __le__(self, other):
		if isinstance(other, Register):
			return False
		
		elif isinstance(other, Mem):
			return self.offset <= other.offset
		
		else:
			return False
	
	def __ne__(self, other):
		if isinstance(other, Mem):
			return self.offset != other.offset
		else:
			return True
	
	def __str__(self):
		return self.formatString.format(self.offset)

class Register(Color):
	def __init__(self, name):
		self.name = name
	
	def __eq__(self, other):
		if isinstance(other, Register):
			return self.name == other.name
		else:
			return False
	
	def __ge__(self, other):
		if isinstance(other, Mem):
			return False
		
		elif isinstance(other, Register):
			return self.name >= other.name
		
		else:
			return False
	
	def __gt__(self, other):
		if isinstance(other, Mem):
			return False
		
		elif isinstance(other, Register):
			return self.name > other.name
		
		else:
			return False
	
	def __lt__(self, other):
		if isinstance(other, Mem):
			return True
		
		elif isinstance(other, Register):
			return self.name < other.name
		
		else:
			return False
	
	def __le__(self, other):
		if isinstance(other, Mem):
			return True
		
		elif isinstance(other, Register):
			return self.name <= other.name
		
		else:
			return False
	
	def __ne__(self, other):
		if isinstance(other, Register):
			return self.name != other.name
		else:
			return True
	
	def __str__(self):
		return '%' + self.name
