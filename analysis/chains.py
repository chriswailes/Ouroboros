"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		Ouroboros
Date:		2010/09/24
Description:	Find relationship chains.
"""

args		= []
prereqs	= ['heapify', 'related']
result	= None
sets		= ['chain']

def init():
	from analysis.pass_manager import register
	register('chains', chains, args, prereqs, result, sets)

def chains(tree):
	syms = []
	
	# Build PhiChains
	for sym in tree.collectSymbols():
		if len(sym['phi-related']) > 0:
			if not sym.has_key('chain'):
				# Create our phi chain.  The constructor will store the
				# reference to the chain in each of its member symbols.
				# This will create the references necessary to avoid having
				# the chain CGed right away.
				
				phiSet = sym['phi-related']
				
				PhiChain(phiSet)
		
		else:
			syms.append(sym)
	
	# Build Chains
	while len(syms) > 0:
		chains	= {}
		syms		= sorted(syms, key = lambda sym: sym['span-start'])
		
		# Build chains from the set of symbols still left.
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
				cond &= chains.has_key(sym1) and len(chains[sym1]) > len(chains[sym0])
				
				if cond:
					chains[sym0] = list(chains[sym1])
			
			# Add this symbol to the end of the chain.
			chains[sym0].append(sym0)
		
		# Find the longest of the chains that we have just built.
		longestChain = []
		
		for chain in chains.values():
			if len(chain) > len(longestChain):
				longestChain = chain
		
		# Create our longest chain.  The constructor will store the reference
		# to the chain in each of its member symbols.  This will create the
		# references necessary to avoid having the chain CGed right away.
		Chain(longestChain)
		
		# Remove the symbols from the longest chain from our symbol table.
		syms = set(syms) - set(longestChain)

###############
# Chain Class #
###############

class BasicChain(object):
	def __init__(self, syms):
		self.syms = list(syms)
		self.mark()
	
	def __iter__(self):
		for sym in self.syms:
			yield sym
	
	def __len__(self):
		return len(self.syms)
	
	def __repr__(self):
		return "{}({})".format(
			self.__class__.__name__,
			self.syms
		)
	
	def getPreColors(self):
		preColors = set()
		
		for sym in self:
			if sym.has_key('precolor') and sym['precolor']:
				preColors.add(sym['precolor'])
		
		return preColors
	
	def interference(self):
		interferingSyms = set()
		
		for sym in self:
			interferingSyms |= sym['interference']
		
		return interferingSyms
	
	def last(self):
		return self.syms[-1]
	
	def mark(self):
		# Give each symbol in the chain a refference to it.
		
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
	
	def join(self, other):
		self.syms += other.syms
		self.mark()
		
		return self
	
	def split(self, sym, splitAfter = False):
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
