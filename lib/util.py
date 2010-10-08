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
	from lib.ast import *
	
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
