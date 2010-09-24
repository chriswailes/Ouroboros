"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/09/20
Description:	The actual register allocation code.
"""

from analysis.related import *

from assembler.coloring import *

from lib.ast import *

def color(program):
	if isinstance(program, Node):
		cf = ColorFactory()
		ig = buildInterferenceGraph(program)
		
		findRelated(program, ig)
		chains = findRelationshipChains(program)
		
		precolor(program, ig)
		
		colorAST(program, cf, ig, chains)
		
		return cf
	else:
		raise Exception('Coloring anything besides a tree is unsupported.')

def calculateMaxConstraint(chain, ig):
	constraints = set([])
	
	for sym in chain:
		constraints = constraints | ig[sym]
	
	return constraints

def clearColoring(tree, cf, ig):
	for sym in tree.collectSymbols():
		sym['color'] = None

def colorAST(node, cf, ig, chains):
	
	#Color new symbol.
	if isinstance(node, Assign):
		sym = node.var.symbol
		
		if not sym.has_key('color') or sym['color'] in symsToColors(ig[sym]) or sym['color'] == None:
			#If the related symbol isn't colored with a register then there
			#might be something better available.  If not, the related
			#symbol's color will still fall out of the ColorFactory.
			
			if sym['related'] != None and isinstance(sym['related']['color'], Register) and \
			not sym['related']['color'] in symsToColors(ig[sym] - set([sym['related']])):
				
				#If the related variable is a register we will take it as
				#as it does not cause interference.
				sym['color'] = sym['related']['color']
			
			else:
				color = None
				
				if sym.has_key('related') and sym['related'] != None:
					color = cf.getColor(calculateMaxConstraint(chains[sym], ig), Register, 0)
					
					if color == None:
						color = cf.getColor(ig[sym])
					
					sym['color'] = color
				
				else:
					sym['color'] = cf.getColor(ig[sym])
	
	#Color the node's children.
	for child in node:
		colorAST(child, cf, ig, chains)

def spill(cf, tree, spillSets):
	cf.clear()
	
	ig = buildInterferenceGraph(tree)
	
	clearColoring(tree, cf, ig)
	precolor(tree, ig)
	
	kicks = []
	
	for symbols0 in spillSets:
		symbols1 = list(symbols0 - set(kicks))
		kick = symbols1.pop(0)
		
		for sym in symbols1:
			if sym['weight'] < kick['weight']:
				kick = sym
		
		kick['color'] = cf.getColor(ig[kick], Mem)
		kicks.append(kick)

def symsToColors(symbols):
	colors = []
	
	for sym in symbols:
		if sym.has_key('color'):
			colors.append(sym['color'])
	
	return set(colors)
