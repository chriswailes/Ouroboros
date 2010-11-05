"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/09/20
Description:	x86 specific coloring code and data structures.
"""

from assembler.coloring import Register, Mem

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
memBaseReg = ebp
memDirection = 'down'

##################################
# Architecture Specific Coloring #
##################################

def precolor(node, ig, cf):
	global interference
	
	if isinstance(node, Div):
		if isinstance(node.left, Symbol):
			node.left['color'] = eax
		
		for sym in node['pre-alive']:
			ig[sym] |= set([interSym0, interSym2])
	
	elif isinstance(node, Function):
		offset = 8
		
		for sym in node.argSymbols:
			sym['color'] = Mem(offset)
			sym['color'].direction = 'up'
			sym['color'].tagged = True
			
			#Advance to the next argument offset.
			offset += 4
	
	elif isinstance(node, FunctionCall):
		#~print("In FunctionCall node")
		#~print("Pre-alive: {0}".format(node['pre-alive']))
		#~print("Post-alive: {0}".format(node['post-alive']))
		
		for sym in node['pre-alive']:
			if sym in node['post-alive']:
				ig[sym] |= interference
	
	for child in node:
		precolor(child, ig, cf)

