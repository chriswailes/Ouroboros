"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/09/01
Description:	Utility functions.
"""

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

def pad(level):
		ret = ""
		
		for i in range(0, level):
			ret += "\t"
		
		return ret
