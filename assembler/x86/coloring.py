"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/09/20
Description:	x86 specific coloring code and data structures.
"""

from assembler.coloring import Register, CALLEE, CALLER, NOUSE

from lib.ast import *
from lib.symbol_table import Symbol

##########
# Colors #
##########

ebp = Register('ebp', NOUSE)
esp = Register('esp', NOUSE)

eax = Register('eax', CALLER)
ebx = Register('ebx', CALLEE)
ecx = Register('ecx', CALLER)
edx = Register('edx', CALLER)
edi = Register('edi', CALLEE)
esi = Register('esi', CALLEE)
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
		
		if isinstance(node.exp, FunctionCall):
			#Here we will pre-color the variable with %eax.  If another
			#function call interferes with the variable the pre-color will be
			#discarded and a new one will be selected.
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
