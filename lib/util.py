"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/09/01
Description:	Utility functions.
"""

#Performs a check to make sure that obj is one of the classes specified.
def classGuard(obj, *klasses):
	for klass in klasses:
		if isinstance(obj, klass):
			return True
	
	return False

def extractSymbol(node):
	from lib.ast import Assign, FunctionCall, Return, Subscript, Symbol, Phi
	
	if isinstance(node, Assign):
		ret = extractSymbol(node.var)
	
	elif isinstance(node, FunctionCall):
		ret = node.name
	
	elif isinstance(node, Phi):
		ret = node.target
	
	elif isinstance(node, Return):
		ret = node.value
	
	elif isinstance(node, Subscript):
		ret = node.symbol
	
	elif isinstance(node, Symbol):
		ret = node
	
	else:
		raise Exception("Node doesn't have a symbol.")
	
	return ret

def flatten(orig):
	new = []
	
	for el0 in orig:
		if el0:
			if classGuard(el0, list, tuple):
				for elt1 in flatten(el0):
					new.append(el1)
			else:
				new.append(el0)
	
	return new

def reType(value):
	from lib.ast import List, Dictionary, Integer, Tru, Fals
	
	if isinstance(value, list):
		return List(value)
	
	elif isinstance(value, dict):
		return Dictionary(value)
	
	elif isinstance(value, int) and not isinstance(value, bool):
		return Integer(value)
	
	elif value is True:
		return Tru()
	
	elif value is False:
		return Fals()
	
	else:
		raise Exception('Unhandled type returned from eval.')

def pad(level):
		ret = ""
		
		for i in range(0, level):
			ret += "\t"
		
		return ret

def substitute(node, callTest, substituteTest, replacement):
	newChildren = []
	
	for child in node:
		if callTest(child):
			newChildren.append(substitute(child, callTest, substituteTest, replacement))
		
		else:
			newChildren.append(child)
	
	node.setChildren(flatten(newChildren))
	
	if substituteTest(node):
		node = replacement(node)
	
	return node

class Enum(object):
	def __init__(self, value):
		self.value = value
	
	def __eq__(self, other):
		return isinstance(other, Enum) and self.value == other.value
	
	def __ne__(self, other):
		return not (self == other)

