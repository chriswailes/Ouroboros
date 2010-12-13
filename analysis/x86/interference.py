"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		Ouroboros
Date:		2010/12/08
Description:	Determines interference for symbols due to architectural hazards.
"""

from lib.ast import *

from assembler.x86.coloring import interference, interSym0, interSym2

def interfere(node):
	if isinstance(node, Div):
		for sym in node['pre-alive']:
			sym['interference'] |= set([interSym0, interSym2])
	
	elif isinstance(node, FunctionCall):
		for sym in node['pre-alive']:
			if sym in node['post-alive']:
				if sym.has_key('interference'):
					sym['interference'] |= interference
				
				else:
					sym['interference'] = interference
	
	for child in node:
		interfere(child)
