"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/09/24
Description:	Find relationship chains.
"""

args		= ['relgraph']
prereqs	= ['related']
result	= 'chains'

def init():
	from analysis.pass_manager import register
	register('chains', chains, args, prereqs, result)

def chains(tree, relgraph):
	
	#~print("Relgraph:")
	#~for sym in relgraph:
		#~print("{0}: {1}".format(sym, relgraph[sym]))
	#~print('')
	
	outerGraph = relgraph.copy()
	
	finalChains = []
	chainDict = {}
	
	#The outer loop finds new starting symbols, and will end when we have
	#produced all of our chains.
	while len(outerGraph) > 0:
		innerGraph = outerGraph.copy()
		sym0 = innerGraph.keys()[0]
		
		#Find the symbol with the earliest definition point among those still
		#remaining.
		for sym1 in innerGraph:
			if sym1['span-start'] < sym0['span-start']:
				sym0 = sym1
		
		chains = {sym0:[sym0]}
		verts = [sym0]
		
		#Build all possible paths using sym0 as the starting vertex.
		while len(verts) > 0:
			sym0 = verts.pop(0)
			
			for sym1 in innerGraph[sym0]:
				chains[sym1] = list(chains[sym0])
				chains[sym1].append(sym1)
				
				verts.append(sym1)
		
		#Locate the longest path found.
		longestChain = []
		for sym in chains:
			if len(longestChain) < len(chains[sym]):
				longestChain = chains[sym]
		
		#Add this to our final list of chains.
		finalChains.append(longestChain)
		
		#Prune the path from the outer graph.
		for sym0 in longestChain:
			del outerGraph[sym0]
			
			for sym1 in outerGraph:
				if sym0 in outerGraph[sym1]:
					outerGraph[sym1].remove(sym0)
	
	#Build the chain dictionary and mark the forward relations.
	for chain in finalChains:
		prevSym = None
		
		for sym in chain:
			sym['related-forward'] = prevSym
			prevSym = sym
			
			chainDict[sym] = chain
	
	return chainDict
