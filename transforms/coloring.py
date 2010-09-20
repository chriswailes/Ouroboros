"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/09/20
Description:	The actual register allocation code.
"""

from analysis.related import findRelatedAST

from assembler.coloring import getColorFactory, interfere, precolor

from lib.ast import *

def color(program):
	if isinstance(program, Node):
		findRelatedAST(program)
		
		cf = getColorFactory()
		ig = buildInterferenceGraph(program)
		
		interfere(program, ig)
		
		colorAST(program, cf, ig)
		
		return cf.offset
	else:
		raise Exception('Coloring anything besides a tree is unsupported.')

def colorAST(node, cf, ig, available = []):
	
	#Get a new color if none are available.
	if len(available) == 0:
		available.append(cf.newColor())
	
	#Color new symbol.
	if isinstance(node, Assign):
		sym = node.var.symbol
		
		if sym['related'] != None:
			sym['color'] = sym['related']['color']
		else:
			sym['color'] = available.pop(0)
		
		print("Assigned color {0} to symbol {1}.".format(sym['color'], sym))
	
	#Color the node's children.
	for child in node:
		available = colorAST(child, cf, ig, available)
	
	#Mark the node with colors that are available for use as temporaries.
	node['temp-colors'] = available
	
	#Free colors from dead symbols.
	for sym in node['pre-alive']:
		if not sym in node['post-alive']:
			available.append(sym['color'])
	
	return available

def buildInterferenceGraph(tree):
	symbols = tree.collectSymbols()
	ig = {}
	
	for sym0 in symbols:
		ig[sym0] = set([])
	
	for sym0 in symbols:
		for sym1 in symbols:
			if sym0 != sym1:
				if sym0['span-start'] <= sym1['span-start'] and sym0['span-end'] >= sym1['span-start']:
					ig[sym0] = ig[sym0] | set([sym1])
					ig[sym1] = ig[sym1] | set([sym0])
	
	return ig
