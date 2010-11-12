"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/09/24
Description:	Determines the liveness of varaibles at every node in the AST.
"""

args		= []
prereqs	= ['spans']
result	= 'ig'

def init():
	from analysis.pass_manager import register
	register('interference', interference, args, prereqs, result)

def interference(tree):
	symbols = tree.collectSymbols()
	ig = {}
	
	for sym0 in symbols:
		ig[sym0] = set([])
	
	for sym0 in symbols:
		print("{0} : {1}".format(sym0, sym0.keys()))
		for sym1 in symbols:
			print("{0} : {1}".format(sym1, sym1.keys()))
			if sym0 != sym1:
				if sym0['span-start'] <= sym1['span-start'] <= sym0['span-end']:
					ig[sym0] = ig[sym0] | set([sym1])
					ig[sym1] = ig[sym1] | set([sym0])
	
	return ig
