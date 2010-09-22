"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/09/20
Description:	The actual register allocation code.
"""

from analysis.related import findRelatedAST

from assembler.coloring import *

from lib.ast import *

def color(program):
	if isinstance(program, Node):
		findRelatedAST(program)
		
		cf = ColorFactory()
		ig = buildInterferenceGraph(program)
		
		precolor(program, ig)
		
		colorAST(program, cf, ig)
		
		return cf
	else:
		raise Exception('Coloring anything besides a tree is unsupported.')

def colorAST(node, cf, ig):
	
	#Color new symbol.
	if isinstance(node, Assign):
		sym0 = node.var.symbol
		
		if sym0['related'] != None and isinstance(sym0['related']['color'], Register):
			#If the related variable is a register we definitely want to
			#take it.
			sym0['color'] = sym0['related']['color']
		
		else:
			#If the related symbol isn't colored with a register then there
			#might be something better available.  If not, the related
			#symbol's color will still fall out of the ColorFactory.
			sym0['color'] = cf.getColor(ig[sym0])
	
	#Color the node's children.
	for child in node:
		colorAST(child, cf, ig)

def buildInterferenceGraph(tree):
	symbols = tree.collectSymbols()
	ig = {}
	
	for sym0 in symbols:
		ig[sym0] = set([])
	
	for sym0 in symbols:
		for sym1 in symbols:
			if sym0 != sym1:
				if sym0['span-start'] <= sym1['span-start'] <= sym0['span-end']:
					ig[sym0] = ig[sym0] | set([sym1])
					ig[sym1] = ig[sym1] | set([sym0])
	
	return ig
