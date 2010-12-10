"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/09/24
Description:	The pass manager for the transformation passes.
"""

from lib.ast import Module

from analysis import pass_manager as apm

class TransformPass(object):
	def __init__(self, fun, analysis, args):
		self.fun		= fun
		self.analysis	= analysis
		self.args		= args

passes = {}

def fixedpoint(tree, addArgs, *transforms):
	before = ''
	after  = repr(tree)
	
	while before != after:
		before = after
		
		for transform in transforms:
			runTransformPrime(tree, addArgs, transform)
		
		after = repr(tree)

def register(name, fun, analysis, args):
	global passes
	passes[name] = TransformPass(fun, analysis, args)

def runTransform(tree, transform, addArgs = {}):
	global passes
	
	if not isinstance(tree, Module):
		raise Exception("Root node of tree wasn't a module.")
	
	if isinstance(transform, list):
		transforms = []
		
		for t in transform:
			transforms.append(passes[t])
		
		fixedpoint(tree, addArgs, *transforms)
	
	else:
		return runTransformPrime(tree, addArgs, passes[transform])

def runTransformPrime(tree, addArgs, transform):
	results = apm.runPasses(tree, transform.analysis)
	results.update(addArgs)
	
	arglist = []
	for arg in transform.args:
		arglist.append(results[arg])
	
	return transform.fun(tree, *arglist)

#####################
# Initialize Passes #
#####################

from transforms import coloring
from transforms import const_fold
from transforms import dead_code
from transforms import dead_store
from transforms import declassify
from transforms import flatten
from transforms import function_migration
from transforms import simplify
from transforms import value_prop

toInit = [coloring, const_fold, dead_code, dead_store, declassify, flatten, function_migration, simplify, value_prop]

for p in toInit:
	p.init()
