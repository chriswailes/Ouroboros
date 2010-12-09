"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		Ouroboros
Date:		2010/12/08
Description:	This file contains a x86 specific precoloring analysis pass.
"""

from lib.ast import *

from assembler.coloring import Mem
from assembler.x86.coloring import eax

def precolor(node):
	if isinstance(node, Div) and isinstance(node.left, Symbol):
		node.left['precolor'] = eax
	
	elif isinstance(node, Function):
		#This clause pre-colors function arguments with their position on the
		#stack relative to the %ebp register.  The first argument starts 8
		#bytes above the base pointer.  Each successive argument is 4 bytes
		#above that.
		
		offset = 8
		
		for sym in node.argSymbols:
			sym['precolor'] = Mem(offset, 'up', True)
			
			#Advance to the next argument offset.
			offset += 4
	
	elif isinstance(node, Return):
		#Values are returned from functions in the %eax register.
		
		node['precolor'] = eax
	
	elif isinstance(node, Symbol) and not node.has_key('precolor'):
		node['precolor'] = None
	
	for child in node:
		precolor(child)
