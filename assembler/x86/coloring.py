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

eax = Register('eax')
ebx = Register('ebx')
ecx = Register('ecx')
edx = Register('edx')
edi = Register('edi')
esi = Register('esi')
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
memFormatString = "-{0:d}(%ebp)"

##################################
# Architecture Specific Coloring #
##################################

def precolor(node, ig):
	global interference
	
	if isinstance(node, FunctionCall):
		for sym in node['pre-alive']:
			ig[sym] = ig[sym] | interference
	
	for child in node:
		precolor(child, ig)
