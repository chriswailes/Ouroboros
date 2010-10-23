"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/09/20
Description:	The actual register allocation code.
"""

from assembler.coloring import *

from lib.ast import *

analysis0	= ['interference', 'related', 'chains', 'heapify']
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
	
	precolor(tree, ig, cf)
	colorPrime(tree, cf, ig, chains)
	
	#~print('Coloring:')
	#~for sym in tree.collectSymbols():
		#~if sym.has_key('color'):
			#~print("{0}: {1}".format(sym, sym['color']))
	#~print('')
	
	return cf

def spill(tree, spillSets, ig):
	cf = ColorFactory()
	
	clearColoring(tree, cf, ig)
	
	#~print('Post-clearing Coloring:')
	#~for sym in tree.collectSymbols():
		#~if sym.has_key('color'):
			#~print("{0}: {1}".format(sym, sym['color']))
	#~print('')
	
	precolor(tree, ig, cf)
	
	#~print('Post-precolor Coloring:')
	#~for sym in tree.collectSymbols():
		#~if sym.has_key('color'):
			#~print("{0}: {1}".format(sym, sym['color']))
	#~print('')
	
	kicks = []
	
	for symbols0 in spillSets:
		symbols1 = list(symbols0 - set(kicks))
		kick = symbols1.pop(0)
		
		for sym in symbols1:
			if sym['weight'] < kick['weight']:
				kick = sym
		
		kick['color'] = cf.getColor(ig[kick], Mem)
		kicks.append(kick)
		print("Kicking {0}".format(kick))
	
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
		sym = node.var
		
		#We need to find a color if the symbol doesn't already have one, or if
		#the color it was pre-colored with interferes with a other colors.
		if not sym.has_key('color') or sym['color'] in toColors(ig[sym]) or sym['heapify']:
			forward  = sym['related-forward']
			backward = sym['related-backward']
			phi = sym['phi-related']
			
			if sym['heapify']:
				sym['color'] = cf.getDataLabel()
			
			elif len(phi) > 0:
				sym['color'] = cf.getColor(maxConstraint(phi, ig))
				
				for sym1 in phi:
					sym1['color'] = sym['color']
			
			elif forward and isinstance(forward['color'], Register) and not forward in toColors(ig[sym] - set([forward])):
				#If our forward looking relation's color is a register and
				#doesn't cause interference we want to use it.
				
				sym['color'] = forward['color']
			
			elif backward and isinstance(backward['color'], Register) and not backward in toColors(ig[sym] - set([backward])):
				#Next we will try our backward looking relation's color.
				
				sym['color'] = backward['color']
			
			else:
				#If all else fails we will get a new color from those that
				#are currently available.
				
				#This is our first attempt at finding a color.  We look at
				#the maximum constraint imposed by the chain that this
				#symbol is a part of, and take our callee/caller preference
				#from the whole chain.  If there is a single symbol that
				#spans a function call we would rather go with a callee
				#saved register.
				color = cf.getColor(maxConstraint(chains[sym], ig), Register, maxPref(chains[sym]))
				
				#If we didn't find a color under maximum constraint we will
				#pick one based solely on this symbols interference graph.
				if color == None:
					color = cf.getColor(ig[sym], preferCaller = not sym['spans-funcall'])
				
				sym['color'] = color
	
	#Color the node's children.
	for child in node:
		colorPrime(child, cf, ig, chains)

def maxConstraint(chain, ig):
	constraints = set([])
	
	for sym in chain:
		constraints = constraints | ig[sym]
	
	return constraints

def maxPref(chain):
	for sym in chain:
		if sym['spans-funcall']:
			return False
	
	return True
