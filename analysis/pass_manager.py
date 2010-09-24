"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/09/24
Description:	The pass manager for the analysis passes.
"""

class AnalysisPass(object):
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
	passes[name] = AnalysisPass(fun, args, prereqs, result)

def runPass(p, tree):
	return runPasses([p], tree)

def runPasses(ps, tree):
	global passes
	
	run = set([])
	remaining = set([])
	results = {}
	
	for p in ps:
		remaining = remaining | findReqs(p)
	
	while len(remaining) != 0:
		toRun = None
		toRunName = ''
		
		for tmp in remaining:
			if len(passes[tmp].prereqs - run) == 0:
				toRun = passes[tmp]
				toRunName = tmp
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
		
		remaining = remaining - set([toRunName])
		run = run | set([toRunName])
	
	return results

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
