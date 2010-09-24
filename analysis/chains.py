"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/09/24
Description:	Find relationship chains.
"""

args		= []
prereqs	= ['related']
result	= 'chains'

def init():
	from analysis.pass_manager import register
	register('chains', chains, args, prereqs, result)

def chains(tree):
	chains = []
	chainDict = {}
	
	for sym in tree.collectSymbols():
		if sym.has_key('related') and sym['related'] != None:
			found = False
			
			for chain in chains:
				if sym['related'] in chain:
					chain.append(sym)
					found = True
					break
			
			if not found:
				chains.append([sym])
	
	for chain in chains:
		for sym in chain:
			chainDict[sym] = chain
	
	return chainDict
