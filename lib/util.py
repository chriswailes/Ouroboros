"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/09/01
Description:	Utility functions.
"""

#Performs a check to make sure that obj is one of the classes specified.
def classGuard(obj, *klasses):
	#~ print("In classGuard.  Obj Class: {0}".format(obj.__class__.__name__))
	for klass in klasses:
		#~ print("Comparing to {0}".format(klass.__name__))
		if isinstance(obj, klass):
			return True
	
	return False

def extractSymbol(node):
	from lib.ast import Assign, Symbol, Subscript, Phi
	
	if isinstance(node, Assign):
		ret = extractSymbol(node.var)
	
	elif isinstance(node, Symbol):
		ret = node
	
	elif isinstance(node, Subscript):
		ret = node.symbol
	
	elif isinstance(node, Phi):
		ret = node.target
	
	else:
		raise Exception("Node doesn't have a symbol.")
	
	return ret

def flatten(seq):
	l = []
	for elt in seq:
		t = type(elt)
		if t is tuple or t is list:
			for elt2 in flatten(elt):
				l.append(elt2)
		else:
			l.append(elt)
	return l

def reType(value):
	from lib.ast import List, Dictionary, Integer, Tru, Fals
	
	if isinstance(value, list):
		return List(value)
	
	elif isinstance(value, dict):
		return Dictionary(value)
	
	elif isinstance(value, int):
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
