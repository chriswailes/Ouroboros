"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		Ouroboros
Date:		2010/09/24
Description:	The pass manager for the analysis passes.
"""

class AnalysisPass(object):
	def __init__(self, fun, args, prereqs, result, sets):
		self.fun		= fun
		self.args		= set(args)
		self.prereqs	= set(prereqs)
		self.result	= result
		self.sets		= set(sets + ['tmp'])

passes = {}

def findReqs(p, reqs = set([])):
	global passes
	
	reqs = reqs | set([p])
	
	for req in passes[p].prereqs:
		reqs = reqs | findReqs(req)
	
	return reqs

def register(name, fun, args, prereqs, result, sets):
	global passes
	passes[name] = AnalysisPass(fun, args, prereqs, result, sets)

def runPass(tree, p):
	return runPasses(tree, [p])

def runPasses(tree, ps):
	global passes
	
	run = set([])
	remaining = set([])
	results = {}
	
	for p in ps:
		remaining |= findReqs(p)
	
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
			tree.unset(*toRun.sets)
			toRun.fun(tree, *arglist)
		
		remaining = remaining - set([toRunName])
		run = run | set([toRunName])
	
	return results

#####################
# Initialize Passes #
#####################

from analysis import chains
from analysis import heapify
from analysis import interference
from analysis import liveness
from analysis import precolor
from analysis import reads
from analysis import related
from analysis import scope
from analysis import spans
from analysis import weight

toInit = [chains, heapify, interference, liveness, precolor, reads, related, scope, spans, weight]

for p in toInit:
	p.init()
