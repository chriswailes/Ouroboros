"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/09/24
Description:	Find relationship chains.
"""

args		= ['']
prereqs	= ['heapify', 'related']
result	= ''
sets		= ['chain']

def init():
	from analysis.pass_manager import register
	register('chains', chains, args, prereqs, result, sets)

def chains(tree):
	syms = set()
	
	#Build PhiChains
	for sym0 in tree.collectSymbols():
		if len(sym0['phi-related']) > 0 and not self.has_key('chain'):
			PhiChain(sym0['phi-related'])
		
		else:
			syms.add(sym)
	
	#Build Chains
	while len(syms) > 0:
		chains	= {}
		syms		= sorted(syms, key = lambda sym: sym['span-start'])
		
		#Build chains from the set of symbols still left.
		for sym0 in syms:
			chains[sym0] = []
			
			for sym1 in sym0['related']:
				
				#We only want to form a chain when:
				#	- The related symbol is still available
				#	- The related symbol isn't going to be heapified
				#	- The chain with sym1 at its end is longer than the
				#		current chain
				
				cond  = sym1 in syms
				cond &= not sym1['heapify']
				cond &= len(chains[sym1]) > len(chains[sym0])
				
				if cond:
					chains[sym0] = chains[sym1].copy()
			
			#Add this symbol to the end of the chain.
			chains[sym0].append(sym0)
		
		#Find the longest of the chains that we have just built.
		longestChain = []
		
		for chain in chains.values():
			if len(chain) > len(longestChain):
				longestChain = chain
		
		longestChain = Chain(longestChain)
		
		#Remove the symbols in the longest chain from our symbol list.
		for sym in longestChain:
			syms.remove(sym)

###############
# Chain Class #
###############

class BasicChain(object):
	def __init__(self, syms):
		self.syms = set(syms)
		
		self.mark()
	
	def __iter__(self):
		for sym in self.syms:
			yield sym
	
	def __len__(self):
		return len(self.syms)
	
	def interference(self):
		interferingSyms = set()
		
		for sym in self:
			interferingSyms |= sym['interference']
		
		return interferingeSyms
	
	def last(self):
		return self.syms[-1]
	
	def mark(self):
		#Give each symbol in the chain a refference to it.
		
		for sym in self.syms:
			sym['chain'] = self
	
	def preferCaller(self):
		for sym in self:
			if sym['spans-funcall']:
				return False
		
		return True

class Chain(BasicChain):
	def add(self, sym):
		self.syms.add(sym)
	
	def getColor(self):
		color = None
		
		for sym in self:
			if sym.has_key('color'):
				if color:
					if color != sym['color']:
						raise Exception('Chain has multiple colors.')
				
				else:
					color = sym['color']
		
		return color
	
	def getPreColors(self):
		preColors = set()
		
		for sym in self:
			if sym['precolor']:
				preColors.add(sym['precolor'])
		
		return preColors
	
	def split(sym, splitAfter = False):
		if sym not in self.syms:
			raise Exception("Trying to split a chain on a symbol that isn't a member.")
		
		index = self.syms.index(sym)
		
		if splitAfter:
			index += 1
		
		old = self.syms[0:index]
		new = self.syms[index:]
		
		self.syms = old
		
		return Chain(new)

class PhiChain(BasicChain):
	def getColors(self):
		colors = set()
		
		for sym in self:
			if sym.has_key('color'):
				colors.add(sym['color'])
		
		return colors
