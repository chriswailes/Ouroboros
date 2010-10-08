"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/09/24
Description:	The pass manager for the transformation passes.
"""

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
from transforms import const_prop
from transforms import discard
from transforms import flatten
from transforms import simplification

toInit = [coloring, const_fold, const_prop, discard, flatten, simplification]

for p in toInit:
	p.init()
