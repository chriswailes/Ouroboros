"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		Ouroboros
Date:		2010/09/20
Description:	Generic assembler coloring classes and functions.
"""

from lib.config import config
from lib.symbol_table import Symbol

def precolor(tree, ig, cf):
	if config.arch == 'x86':
		from x86.coloring import precolor
	elif config.arch == 'x86_64':
		from x86_64.coloring import precolor
	
	precolor(tree, ig, cf)

def toColors(l):
	colors = set()
	
	for o in l:
		if isinstance(o, Color):
			colors.add(o)
		
		elif isinstance(o, Symbol) and o.has_key('color') and o['color']:
			colors.add(o['color'])
	
	return colors

class ColorFactory(object):
	def __init__(self):
		self.offset = 0
		
		if config.arch == 'x86':
			from x86.coloring import colors, preIncrement, wordSize
		elif config.arch == 'x86_64':
			from x86_64.coloring import colors, preIncrement, wordSize
		
		from assembler.ib import Labeler, Label
		
		self.colors = set(colors)
		self.preIncrement = preIncrement
		self.labeler = Labeler('D')
		self.wordSize = wordSize
	
	def clear(self):
		regs = []
		
		for color in self.colors:
			if isinstance(color, Register):
				regs.append(color)
		
		self.colors = set(regs)
		self.offset = 0
	
	def getColor(self, interference = set(), test = None, preferCaller = False):
		color = None
		
		if preferCaller:
			self.swapPreference()
		
		allocated = toColors(interference)
		free = self.colors - allocated
		
		if test != None:
			filteredFree = []
			
			for colour in free:
				if isinstance(colour, test):
					filteredFree.append(colour)
			
			free = filteredFree
		
		else:
			free = list(free)
		
		if len(free) > 0:
			free.sort()
			color = free[0]
		
		elif test != Register:
			
			if self.preIncrement:
				self.offset += self.wordSize
			
			color = Mem(self.offset)
			
			if not self.preIncrement:
				self.offset += self.wordSize
			
			self.colors = self.colors | set([color])
		
		if preferCaller:
			self.swapPreference()
		
		return color
	
	def getDataLabel(self, reference = False):
		return self.labeler.nextLabel(reference)
	
	def swapPreference(self):
		for color in self.colors:
			if isinstance(color, Register):
				if color.weight == 0:
					color.weight = 1
				
				else:
					color.weight = 0

class Color(object):
	def __repr__(self):
		return str(self)

class Mem(Color):
	def __init__(self, offset, direction = None, tagged = False):
		self.offset = offset
		
		self.formatString = "{0}{1:d}({2})"
		
		self.tagged = tagged
		self.tag = None
		
		if config.arch == 'x86':
			from x86.coloring import memBaseReg, memDirection
		elif config.arch == 'x86_64':
			from x86_64.coloring import memBaseReg, memDirection
		
		self.baseReg = memBaseReg
		self.direction = direction or memDirection
	
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
		return self.formatString.format('' if self.direction == 'up' else '-', self.offset, self.baseReg)

class Register(Color):
	def __init__(self, name, weight):
		self.name = name
		self.weight = weight
		
		self.tagged = False
		self.tag = None
	
	def __eq__(self, other):
		if isinstance(other, Register):
			return self.name == other.name
		else:
			return False
	
	def __ge__(self, other):
		if isinstance(other, Mem):
			return False
		
		elif isinstance(other, Register):
			return self.weight >= other.weight or (self.weight == other.weight and self.name >= other.name)
		
		else:
			return False
	
	def __gt__(self, other):
		if isinstance(other, Mem):
			return False
		
		elif isinstance(other, Register):
			return self.weight > other.weight or (self.weight == other.weight and self.name > other.name)
		
		else:
			return False
	
	def __le__(self, other):
		if isinstance(other, Mem):
			return True
		
		elif isinstance(other, Register):
			return self.weight <= other.weight or (self.weight == other.weight and self.name <= other.name)
		
		else:
			return False
	
	def __lt__(self, other):
		if isinstance(other, Mem):
			return True
		
		elif isinstance(other, Register):
			return self.weight < other.weight or (self.weight == other.weight and self.name < other.name)
		
		else:
			return False
	
	def __ne__(self, other):
		if isinstance(other, Register):
			return self.weight != other.weight or self.name != other.name
		else:
			return True
	
	def __str__(self):
		return '%' + self.name
	
	def clear(self):
		self.tagged = False
		self.tag = None
