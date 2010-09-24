"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/09/20
Description:	The actual register allocation code.
"""

from assembler.coloring import *

from lib.ast import *

analysis0	= ['interference', 'related', 'chains']
args0	= ['ig', 'chains', 'cf']

analysis1	= ['interference', 'related', 'weight']
args1	= ['spillSets', 'ig']

def init():
	from transforms.pass_manager import register
	register('color', color, analysis0, args0)
	register('spill', spill, analysis1, args1)

##################
# Main Functions #
##################

def color(tree, ig, chains, cf = None):
	cf = cf or ColorFactory()
	
	precolor(tree, ig)
	colorPrime(tree, cf, ig, chains)
	
	return cf

def spill(tree, spillSets, ig):
	cf = ColorFactory()
	
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
	
	return cf

####################
# Helper Functions #
####################

def clearColoring(tree, cf, ig):
	for sym in tree.collectSymbols():
		del sym['color']

def colorPrime(node, cf, ig, chains):
	#Color new symbol.
	if isinstance(node, Assign):
		sym = node.var.symbol
		
		if not sym.has_key('color') or sym['color'] in symsToColors(ig[sym]):
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
					color = cf.getColor(maxConstraint(chains[sym], ig), Register, 0)
					
					if color == None:
						color = cf.getColor(ig[sym])
					
					sym['color'] = color
				
				else:
					sym['color'] = cf.getColor(ig[sym])
	
	#Color the node's children.
	for child in node:
		colorPrime(child, cf, ig, chains)

def maxConstraint(chain, ig):
	constraints = set([])
	
	for sym in chain:
		constraints = constraints | ig[sym]
	
	return constraints

def symsToColors(symbols):
	colors = []
	
	for sym in symbols:
		if sym.has_key('color'):
			colors.append(sym['color'])
	
	return set(colors)
