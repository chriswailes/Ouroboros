"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/09/018
Description:	Finds related symbols.
"""

from lib.ast import *

def findRelated(node, ig):
	if isinstance(node, Assign):
		sym0 = node.var.symbol
		sym0['related'] = None
		
		if isinstance(node.exp, Name):
			sym1 = node.exp.symbol
			
			if not sym1 in node['post-alive']:
				print("Marking {0} as related to {1}".format(sym0, sym1))
				sym0['related'] = sym1
		
		elif isinstance(node.exp, BinOp):
			sym1 = None
			
			if isinstance(node.exp.left, Name):
				sym1 = node.exp.left.symbol
			
			elif isinstance(node.exp.right, Name) and (isinstance(node.exp, Add) or isinstance(node.exp, Mul)):
				sym1 = node.exp.right.symbol
			
			if sym1 and not sym1 in node['post-alive']:
				print("Marking {0} as related to {1}".format(sym0, sym1))
				sym0['related'] = sym1
		
		elif isinstance(node.exp, UnaryOp) and isinstance(node.exp.operand, Name):
			sym1 = node.exp.operand.symbol
			
			if not sym1 in node['post-alive']:
				print("Marking {0} as related to {1}".format(sym0, sym1))
				sym0['related'] = sym1
	
	for child in node:
		findRelated(child, ig)

def findRelationshipChains(tree):
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
	
	print("Relationship Chains:")
	for sym in chainDict:
		print("\t{0} -> {1}".format(sym, chainDict[sym]))
	
	return chainDict
			
