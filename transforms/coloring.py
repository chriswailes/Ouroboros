"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		Ouroboros
Date:		2010/09/20
Description:	The actual register allocation code.
"""

from analysis.chains import Chain, PhiChain

from assembler.coloring import *

from lib.ast import *

analysis0	= ['interference', 'related', 'chains', 'heapify', 'spans', 'precolor']
args0	= ['cf']

analysis1	= ['interference', 'weight', 'precolor']
args1	= ['spillSets']

def init():
	from transforms.pass_manager import register
	register('color', color, analysis0, args0)
	register('spill', spill, analysis1, args1)

##################
# Main Functions #
##################

def color(tree, cf):
	
	###################
	# String Coloring #
	###################
	
	for string in tree.strings:
		tree.strings[string]['color'] = cf.getDataLabel(True)
	
	###################
	# Symbol Coloring #
	###################
	
	syms = sorted(tree.collectSymbols(), key = lambda sym: sym['span-start'])
	
	for sym in syms:
		if not sym.has_key('color'):
			chain		= sym['chain']
			interference	= toColors(sym['interference'] - set(chain.syms))
			preference	= not sym['spans-funcall']
			preColors		= list(chain.getPreColors())
			
			color = None
			
			if sym['heapify']:
				# Coloring heapified symbols is easy.  Just give them a
				# label.
				color = cf.getDataLabel()
			
			elif sym['precolor'] and isinstance(sym['precolor'], Mem):
				# If the precolor is a memory location that means that the
				# symbol is a function argument.  Therefor we must take its
				# precolor as its color.
				
				color = sym['precolor']
			
			elif isinstance(chain, PhiChain):
				# Here we will try and give all phi-related symbols the
				# same color.
				
				colors = list(chain.getColors())
				
				if len(colors) == 0:
					# When there are no colors currently assigned to any
					# of the symbols we will try and get a new one that
					# meets the maximum constraint of all the symbols.
					
					if len(preColors) == 1 and isinstance(preColors[0], Register) and preColors[0] not in chain.interference():
						color = preColors[0]
					
					elif sym['precolor'] and sym['precolor'] not in interference:
						color = sym['precolor']
					
					elif len(preColors) > 1:
						for c in preColors:
							if c not in chain.interferenece():
								color = c
								break
						
					
					if not color:
						color = cf.getColor(chain.interference(), Register, chain.preferCaller())
				
				elif len(colors) == 1:
					# So far the phi-related symbols only have one color
					# between them.  We will see if it causes
					# interference, and if not, we will use it.
					
					if isinstance(colors[0], Register) and colors[0] not in interference:
						color = colors[0]
				
				else:
					# There are several choices in colors from this
					# symbol's phi-relatives.  If any of them work we will
					# use them.
					
					for c in colors:
						if c not in interference and isinstance(c, Register):
							color = c
							break
			
			else:
				
				color = chain.getColor()
				
				if not color:
					# This chain doesn't have a color yet.  Try and get
					# one that meets the constraints of every symbol in
					# the chain.
					
					
					if len(preColors) == 1 and preColors[0] not in chain.interference():
						color = preColors[0]
					
					elif sym['precolor'] and sym['precolor'] not in interference:
						color = sym['precolor']
					
					elif len(preColors) > 1:
						for c in preColors:
							if c not in chain.interferenece():
								color = c
								break
					
					if not color:
						color = cf.getColor(chain.interference(), Register, preferCaller = chain.preferCaller())
				
				elif isinstance(color, Mem) or color in interference:
					# The color of the chain isn't any good.  Try and find
					# a different chain to become a part of, or start a
					# new one.
					
					newChain = chain.split(sym)
					related = sym['related']
					
					if len(related) == 2:
						first, last = related
						altChain = first['chain'] if first['chain'] != chain else last['chain']
						
						c = altChain.getColor()
						
						if c and c not in newChain.interference():
							color = c
							altChain.join(newChain)
			
			# If we didn't find a color any of the other ways we will get a
			# new one.
			if not color:
				color = cf.getColor(interference, preferCaller = preference)
			
			if isinstance(chain, PhiChain):
				color.tagged = True
		
			sym['color'] = color
	
		#~print("Coloring {} with {}\n".format(sym, sym['color']))
	
	return cf

def spill(tree, spillSets):
	cf = ColorFactory()
	
	tree.unset('color')
	
	kicks = set()
	
	for syms0 in spillSets:
		syms1 = syms0 - kicks
		
		kick = None
		
		for sym in syms1:
			if not kick or sym['weight'] < kick['weight']:
				kick = sym
		
		kick['color'] = cf.getColor(kick['interference'], Mem)
		
		kicks.add(kick)
	
	return cf
