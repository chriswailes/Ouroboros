"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/09/20
Description:	x86 specific coloring code and data structures.
"""

from assembler.coloring import Register

from lib.ast import *
from lib.symbol_table import Symbol

##########
# Colors #
##########

ebp = Register('ebp', 2)
esp = Register('esp', 2)

eax = Register('eax', 1)
ebx = Register('ebx', 0)
ecx = Register('ecx', 1)
edx = Register('edx', 1)
edi = Register('edi', 0)
esi = Register('esi', 0)

callee = [ebx, edi, esi]
caller = [eax, ecx, edx]
colors = [eax, ebx, ecx, edx, edi, esi]

########################
# Interference Symbols #
########################

interSym0 = Symbol('!INTERFERE0', -1)
interSym0['color'] = eax

interSym1 = Symbol('!INTERFERE1', -1)
interSym1['color'] = ecx

interSym2 = Symbol('!INTERFERE2', -1)
interSym2['color'] = edx

interference = set([interSym0, interSym1, interSym2])

###########################
# ColorFactory Parameters #
###########################

wordSize = 4
preIncrement = True
memFormatString = "-{0:d}(%ebp)"

##################################
# Architecture Specific Coloring #
##################################

def precolor(node, ig):
	global interference
	
	if isinstance(node, Assign):
		sym = node.var.symbol
		
		if isinstance(node.exp, FunctionCall) and not sym.has_key('color'):
			#Here we will pre-color the variable with %eax.  If another
			#function call interferes with the variable the pre-color will
			#be discarded and a new one will be selected.
			sym['color'] = eax
		
		else:
			precolor(node.exp, ig)
	
	elif isinstance(node, FunctionCall):
		for sym in node['pre-alive']:
			if sym in node['post-alive']:
				ig[sym] = ig[sym] | interference
	
	else:
		for child in node:
			precolor(child, ig)

