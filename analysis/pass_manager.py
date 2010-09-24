"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/09/22
Description:	The pass manager for the analysis passes.
"""

class Pass(object):
	def __init__(self, fun, args, prereqs, result):
		self.fun		= fun
		self.args		= set(args)
		self.prereqs	= set(prereqs)
		self.result	= result

passes = {}

def findReqs(p, reqs = set([])):
	global passes
	
	reqs = reqs | set([p])
	
	for req in passes[p].prereqs:
		reqs = reqs | findReqs(req)
	
	return reqs

def register(name, fun, args, prereqs, result):
	global passes
	passes[name] = Pass(fun, args, prereqs, result)

def runPass(p, tree):
	runPasses([p], tree)

def runPases(ps, tree):
	global passes
	
	run = set([])
	remaining = set([])
	results = {}
	
	for p in ps:
		remaining = remaining | findRegs(p)
	
	while len(remaining) != 0:
		toRun = None
		
		for tmp in remaining:
			if len(passes[tmp].prereqs - run) == 0:
				print("Running pass {0}".format(tmp))
				toRun = passes[tmp]
				break
		
		if toRun == None:
			raise Exception("Dependency resolution error: {0}".format(p))
		
		arglist = []
		for arg in toRun.args:
			arglist.append(results[arg])
		
		if toRun.result:
			results[toRun.result] = toRun.fun(tree, *arglist)
		
		else:
			toRun.fun(tree, *arglist)
		
		remaining = remaining - set([toRun])
		run = run | set([toRun])

#####################
# Initialize Passes #
#####################

from analysis import chains
from analysis import interference
from analysis import liveness
from analysis import reads
from analysis import related
from analysis import spans
from analysis import weight

toInit = [chains, interference, liveness, reads, related, spans, weight]

for p in toInit:
	p.init()
