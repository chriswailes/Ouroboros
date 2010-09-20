"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/09/20
Description:	Finds a fixed point in a series of AST transformations.
"""

def fixedpoint(tree, *transforms):
	before = ''
	after  = repr(tree)
	
	while before != after:
		before = after
		
		for transform in transforms:
			tree = transform(tree)
		
		after = repr(tree)
	
	return tree
