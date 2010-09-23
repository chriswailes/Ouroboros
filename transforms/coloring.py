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
		cf = ColorFactory()
		ig = buildInterferenceGraph(program)
		
		findRelatedAST(program, ig)
		
		precolor(program, ig)
		
		colorAST(program, cf, ig)
		
		return cf
	else:
		raise Exception('Coloring anything besides a tree is unsupported.')

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

def clearColoring(tree, cf, ig):
	for sym in tree.collectSymbols():
		if isinstance(sym['color'], Mem):
			sym['color'] = cf.getColor(ig[sym], Mem)
		
		else:
			sym['color'] = None

def colorAST(node, cf, ig):
	
	#Color new symbol.
	if isinstance(node, Assign):
		sym = node.var.symbol
		
		if not sym.has_key('color') or sym['color'] == None:
			if sym['related'] != None and isinstance(sym['related']['color'], Register):
				#If the related variable is a register we definitely want to
				#take it.
				print("Assigning relative {0} to {1}".format(sym['related'], sym))
				#print(ig[sym])
				sym['color'] = sym['related']['color']
			
			else:
				#If the related symbol isn't colored with a register then there
				#might be something better available.  If not, the related
				#symbol's color will still fall out of the ColorFactory.
				print("Coloring {0}: {1}".format(sym, ig[sym]))
				sym['color'] = cf.getColor(ig[sym])
	
	#Color the node's children.
	for child in node:
		colorAST(child, cf, ig)

def spill(cf, tree, symbols):
	cf.clear()
	
	ig = buildInterferenceGraph(tree)
	
	clearColoring(tree, cf, ig)
	precolor(tree, ig)
	
	kick = list(symbols).pop(0)
	
	for sym in symbols:
		if sym['weight'] < kick['weight']:
			kick = sym
	
	for sym in ig:
		print("{0}: {1}".format(sym, ig[sym]))
	
	print('')
	
	kick['color'] = cf.getColor(ig[kick], Mem)
