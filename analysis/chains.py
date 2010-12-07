"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/09/24
Description:	Find relationship chains.
"""

args		= ['']
prereqs	= ['related']
result	= ''
sets		= ['chain']

def init():
	from analysis.pass_manager import register
	register('chains', chains, args, prereqs, result, sets)

def chains(tree):
	syms = tree.collectSymbols()
	
	while len(outerSyms) > 0:
		chains	= {}
		syms		= sorted(syms, key = lambda sym: sym['span-start'])
		
		#Build chains from the set of symbols still left.
		for sym0 in syms:
			chains[sym0] = []
			
			for sym1 in sym0['related']:
				if len(chains[sym1]) > len(chains[sym0]):
					chains[sym0] = chains[sym1].copy()
			
			#Add this symbol to the end of the chain.
			chains[sym0].append(sym0)
		
		#Find the longest of the chains that we have just built.
		longestChain = []
		
		for chain in chains.values():
			if len(chain) > len(longestChain):
				longestChain = chain
		
		longestChain = Chain(longestChain)
		
		#Remove the symbols in the longest chain from our symbol list, and
		#give each one a refference to the chain they are a part of.
		for sym in longestChain:
			syms.remove(sym)
			
			sym['chain'] = longestChain

###############
# Chain Class #
###############

class Chain(object):
	def __init__(self, syms):
		self.syms = set(syms)
	
	def __iter__(self):
		for sym in self.syms:
			yield sym
	
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
