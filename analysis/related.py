"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/09/18
Description:	Finds related symbols.
"""

from lib.ast import *

args		= []
prereqs	= ['liveness', 'spans']
result	= None

def init():
	from analysis.pass_manager import register
	register('related', newRelated, args, prereqs, result)

def related(node):
	if isinstance(node, Assign):
		sym0 = node.var.symbol
		sym0['related'] = None
		
		if isinstance(node.exp, Name):
			sym1 = node.exp.symbol
			
			if not sym1 in node['post-alive']:
				sym0['related'] = sym1
		
		elif isinstance(node.exp, BinOp):
			sym1 = None
			
			if isinstance(node.exp.left, Name):
				sym1 = node.exp.left.symbol
				
				#~if isinstance(node.exp.right, Name) and (isinstance(node.exp, Add) or isinstance(node.exp, Mul)):
					#~sym2 = node.exp.right.symbol
					#~
					#~if sym2['span'] < sym1['span']:
						#~sym1 = sym2
			
			elif isinstance(node.exp.right, Name) and (isinstance(node.exp, Add) or isinstance(node.exp, Mul)):
				sym1 = node.exp.right.symbol
			
			if sym1 and not sym1 in node['post-alive']:
				sym0['related'] = sym1
		
		elif isinstance(node.exp, UnaryOp) and isinstance(node.exp.operand, Name):
			sym1 = node.exp.operand.symbol
			
			if not sym1 in node['post-alive']:
				sym0['related'] = sym1
	
	for child in node:
		related(child)


def newRelated(tree):
	
	print("Starting my new relationship calculating algorithm.")
	
	outerGraph = buildRelationshipGraph(tree)
	innerGraph = outerGraph.copy()
	
	finalChains = []
	
	while len(outerGraph) > 0:
		print("OuterGraph length: {0}".format(len(outerGraph)))
		longestChain = []
		chains = []
		
		while len(innerGraph) > 0:
			print("InnerGraph length: {0}".format(len(innerGraph)))
			start = innerGraph.keys()[0]
			for sym in innerGraph:
				if sym['span-start'] < start['span-start']:
					start = sym
			
			verts = [start]
			newVerts = []
			
			for vert0 in verts:
				print("Visiting {0}".format(vert0))
				newVerts.extend(innerGraph[vert0])
				
				newChains = []
				
				oldChain = [vert0]
				for chain in chains:
					if vert0 in chain:
						oldChain = chain
				
				for index in range(0, len(innerGraph[vert0])):
					if index == 0:
						oldChain.append(innerGraph[vert0][index])
						print("Appended to an old chain: {0}".format(oldChain))
					
					else:
						newChain = list(oldChain)
						newChain.append(vert1)
						print("Split chain: {0}".format(newChain))
						
						newChains.append(newChain)
				
				del innerGraph[vert0]
				chains.extend(newChains)
			
		for chain in chains:
			if len(chain) > len(longestChain):
				longestChain = chain
		
		print("Found longest chain: {0}".format(longestChain))
		
		if longestChain != []:
			finalChains.append(longestChain)
		
		for vert0 in longestChain:
			del outerGraph[vert0]
			
			for vert1 in outerGraph:
				if vert0 in outerGraph[vert1]:
					outerGraph[vert1].remove(vert0)
		
		innerGraph = outerGraph.copy()
	
	print('Chains:')
	print(finalChains)
	print('')
	related(tree)

def buildRelationshipGraph(node, graph = {}):
	if isinstance(node, Assign):
		sym0 = node.var.symbol
		graph[sym0] = []
		
		if isinstance(node.exp, Name):
			sym1 = node.exp.symbol
			
			if not sym1 in node['post-alive']:
				graph[sym1].append(sym0)
		
		elif isinstance(node.exp, BinOp):
			sym1 = None
			
			if isinstance(node.exp.left, Name):
				sym1 = node.exp.left.symbol
				
				if not sym1 in node['post-alive']:
					graph[sym1].append(sym0)
			
			if isinstance(node.exp.right, Name) and (isinstance(node.exp, Add) or isinstance(node.exp, Mul)):
				sym1 = node.exp.right.symbol
				
				if not sym1 in node['post-alive']:
					graph[sym1].append(sym0)
		
		elif isinstance(node.exp, UnaryOp) and isinstance(node.exp.operand, Name):
			sym1 = node.exp.operand.symbol
			
			if not sym1 in node['post-alive']:
				graph[sym1].append(sym0)
	
	for child in node:
		buildRelationshipGraph(child, graph)
	
	return graph
