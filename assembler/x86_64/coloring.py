"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/09/21
Description:	x86_64 specific coloring code and data structures.
"""

from assembler.coloring import Register

from lib.ast import *
from lib.symbol_table import Symbol

##########
# Colors #
##########

rax = Register('rax')
rbx = Register('rbx')
rcx = Register('rcx')
rdx = Register('rdx')
rdi = Register('rdi')
rsi = Register('rsi')
rbp = Register('rbp')
r8  = Register('r8' )
r9  = Register('r9' )
r10 = Register('r10')
r11 = Register('r11')
r12 = Register('r12')
r13 = Register('r13')
r14 = Register('r14')
r15 = Register('r15')
colors = [rax, rbx, rcx, rdx, rdi, rsi, rbp, r8, r9, r10, r11, r12, r13, r14, r15]
args   = [rdi, rsi, rdx, rcx, r8, r9]

########################
# Interference Symbols #
########################

interSym0 = Symbol('!INTERFERE0', -1)
interSym0['color'] = rax

interSym1 = Symbol('!INTERFERE1', -1)
interSym1['color'] = rcx

interSym2 = Symbol('!INTERFERE2', -1)
interSym2['color'] = rdx

interSym3 = Symbol('!INTERFERE3', -1)
interSym3['color'] = rsi

interSym4 = Symbol('!INTERFERE4', -1)
interSym4['color'] = rdi

interSym5 = Symbol('!INTERFERE5', -1)
interSym5['color'] = r8

interSym6 = Symbol('!INTERFERE6', -1)
interSym6['color'] = r9

interSym7 = Symbol('!INTERFERE7', -1)
interSym7['color'] = r10

interSym8 = Symbol('!INTERFERE8', -1)
interSym8['color'] = r11

interference = set([interSym0, interSym1, interSym2, interSym3, interSym4, interSym5, interSym6, interSym7, interSym8])

###########################
# ColorFactory Parameters #
###########################

wordSize = 8
memFormatString = "{0:d}(%rsp)"

##################################
# Architecture Specific Coloring #
##################################

def precolor(tree, ig):
	global args, interference
	
	if isinstance(node, FunctionCall):
		for sym in node['pre-alive']:
			ig[sym] = ig[sym] | interference
		
		index = 0
		for sym in node.args:
			if not sym in node['post-alive']:
				sym['color'] = args[index]
			
			index += 1
			
			if index == len(args):
				break
	
	for child in node:
		precolor(child, ig)
