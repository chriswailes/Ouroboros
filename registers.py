"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/08/26
Description:	Functions and data structures for allocating registers.
"""

allocated = []
available = ["%eax", "%ebx", "%ecx", "%edx"]

def alloc():
	global allocated
	global available
	
	if not allInUse():
		reg = available.pop(0)
		allocated.append(reg)
		
		return reg
	else:
		raise Exception("All registers are currently allocated.")

def allInUse():
	global available
	return len(available) == 0

def inUse(reg):
	global allocated
	return reg in allocated

def free(reg):
	global allocated
	global available
	
	if reg in allocated:
		allocated.remove(reg)
		
		available.append(reg)
		available.sort()
	else:
		raise Exception("Attempting to free an un-allocated register")
