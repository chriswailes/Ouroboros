"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/09/018
Description:	Determines the liveness of varaibles at every node in the AST.
"""

from lib.ast import *

def livenessAST(node, alive = []):
	node['pre-alive'] = set(alive)
	
	if isinstance(node, Assign):
		sym = node.var.symbol
		sym['tmp'] = sym['reads']
		
		if sym['tmp'] > 0:
			alive.append(sym)
	
	elif isinstance(node, Name):
		node.symbol['tmp'] -= 1
		
		if node.symbol['tmp'] == 0:
			alive.remove(name.symbol)
	
	else:
		for n in node:
			livenessAST(n, alive)
	
	node['post-alive'] = set(alive)
	
	print("pre-alive: " + str(node['pre-alive']))
	print("post-alive: " + str(node['post-alive']))
	print('')


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
