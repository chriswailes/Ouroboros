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

rsp = Register('rsp', 2)

rax = Register('rax', 1)
rbx = Register('rbx', 0)
rcx = Register('rcx', 0)
rdx = Register('rdx', 0)
rdi = Register('rdi', 0)
rsi = Register('rsi', 0)
rbp = Register('rbp', 1)
r8  = Register('r8',  0)
r9  = Register('r9',  0)
r10 = Register('r10', 0)
r11 = Register('r11', 0)
r12 = Register('r12', 1)
r13 = Register('r13', 1)
r14 = Register('r14', 1)
r15 = Register('r15', 1)

callee = [rbx, rbp, r12, r13, r14, r15]
caller = [rax, rcx, rdx, rdi, rsi, r8, r9, r10, r11]
args   = [rdi, rsi, rdx, rcx, r8, r9]
colors = [rax, rbx, rcx, rdx, rdi, rsi, rbp, r8, r9, r10, r11, r12, r13, r14, r15]

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
preIncrement = False
memFormatString = "{0:d}(%rsp)"

##################################
# Architecture Specific Coloring #
##################################

def precolor(node, ig):
	global args, interference
	
	if isinstance(node, Assign):
		sym = node.var.symbol
		
		#This causes a lot more pushes and pops across function calls at the
		#moment.
		
		#~if isinstance(node.exp, FunctionCall) and not sym.has_key('color'):
			#~#Here we will pre-color the variable with %rax.  If another
			#~#function call interferes with the variable the pre-color will
			#~#be discarded and a new one will be selected.
			#~sym['color'] = rax
		#~
		#~else:
		
		precolor(node.exp, ig)
	
	elif isinstance(node, FunctionCall):
		for sym in node['pre-alive']:
			if sym in node['post-alive']:
				ig[sym] = ig[sym] | interference
		
		#This is currently left out because it causes too many pushes and pops.
		#~index = 0
		#~for arg in node.args:
			#~if isinstance(arg, Name):
				#~sym = arg.symbol
				#~if not (sym.has_key('color') or sym in node['post-alive']):
					#~sym['color'] = args[index]
			#~
			#~index += 1
			#~
			#~if index == len(args):
				#~break
	
	else:
		for child in node:
			precolor(child, ig)

