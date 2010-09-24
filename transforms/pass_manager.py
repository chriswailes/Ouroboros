"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/09/24
Description:	The pass manager for the transformation passes.
"""

from transforms.fixedpoint import fixedpoint

class TransformPass(object):
	def __init__(self, fun, analysis, args):
		self.fun		= fun
		self.analysis	= analysis
		self.args		= args

transforms = {}

def register(name, fun, analysis, args):
	global transforms
	transforms[name] = TransformPass(fun, analysis, args)

def runTransform(transform):
	pass

def runTransforms():
	pass

#####################
# Initialize Passes #
#####################

from transforms import coloring
from transforms import const_fold
from transforms import const_prop
from transforms import discard
from transforms import flatten

toInit = [coloring, const_fold, const_prop, discard, flatten]

for p in toInit:
	p.init()
