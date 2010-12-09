"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		Ouroboros
Date:		2010/09/24
Description:	Determines interference for symbols both due to overlapping live
			ranges as well as architectural hazards.
"""

args		= []
prereqs	= ['spans']
result	= ''
sets		= ['interference']

from lib.config import config

def init():
	from analysis.pass_manager import register
	register('interference', interfere, args, prereqs, result, sets)

def interfere(tree):
	symbols = tree.collectSymbols()
	
	for sym0 in symbols:
		sym0['interference'] = set()
	
	for sym0 in symbols:
		for sym1 in symbols:
			if sym0 != sym1:
				if sym0['span-start'] <= sym1['span-start'] <= sym0['span-end']:
					sym0['interference'].add(sym1)
					sym1['interference'].add(sym0)
	
	if config.arch == 'x86':
		from x86 import interference as arch
	
	elif config.arch == 'x86_64':
		from x86_64 import interference as arch
	
	arch.interfere(tree)
