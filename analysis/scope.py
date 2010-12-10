"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		Ouroboros
Date:		2010/11/07
Description:	Determins the scope of variables.
"""

from lib.ast import *
from lib.util import classGuard

args		= []
prereqs	= []
result	= None
sets		= ['scope']

def init():
	from analysis.pass_manager import register
	register('scope', scope, args, prereqs, result, sets)

#This analysis pass marks any new symbols as either 'global' or 'local'.  Global
#symbols are defined in the main function and can be put in the data
#section.  Local variables that apear as free variables in lambda
#definitions need to be packed into a closure.
def scope(node, outerScope = None):
	if isinstance(node, Function):
		outerScope = node.name
		
		#Main doesn't have any arguments, so all function arguments can be
		#marked 'local'
		for sym in node.argSymbols:
			sym['scope'] = 'local'
	
	elif classGuard(node, Assign, Phi):
		sym = extractSymbol(node)
		
		sym['scope'] = 'global' if outerScope.name == 'main' else 'local'
	
	for child in node:
		scope(child, outerScope)
