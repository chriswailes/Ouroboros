"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/09/018
Description:	Determines the liveness of varaibles at every node in the AST.
"""

from lib.ast import *

def livenessAST(node, counts, alive = []):
	node['pre-alive'] = set(alive)
	
	if isinstance(node, Assign):
		sym = node.var.name
		if counts[sym] > 0:
			alive.append(node.var.name)
	
	elif isinstance(node, Name):
		counts[name.name] -= 1
		if counts[name.name] == 0:
			alive.remove(name.name)
	
	else:
		for n in node:
			livenessAST(n, counts, alive)
	
	node['post-alive'] = set(alive)


def livenessAssembly(block):
	index = block.getNumInsts()
	indexes = range(0,index)
	indexes.reverse()
	
	alive = set([])
	
	for index in indexes:
		inst = block.getInst(index)
		
		inst.post_alive = alive
		
		reads = None
		writes = None
		
		if isinstance(inst, OneOp):
			reads = set([inst.dest])
		
		elif isinstance(inst, TwoOp):
			if inst.name == 'mov':
				reads = set([inst.src])
				writes = set([inst.dest])
			
			else:
				reads = set([inst.src, inst.dest])
				writes = set([inst.dest])
		
		alive = (alive - writes) | reads
		
		inst.pre_alive = alive
