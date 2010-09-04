"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/08/23
Description:	Describes the abstract syntax tree used by my compiler for HW0.
"""

import util

class Node(object):
	def __iter__(self):
		for n in self.getChildren():
			yield n
	
	def getAttr(self, key):
		return self.attributes[key]
	
	def isSimple(self):
		False
	
	def setAttr(self, key, value):
		self.attributes[key] = value

class Module(Node):
	def __init__(self, stmts):
		self.stmts = stmts
	
	def __repr__(self):
		return "Module({0})".format(repr(self.stmts))
	
	def getChildren(self):
		return self.statements
	
	def toGraph(self):
		pass
	
	def toPython(self):
		module = ""
		
		for s in self.stmts:
			module += s.toPython() + "\n"
		
		return module

class Statement(Node):
	pass

class Assign(Statement):
	def __init__(self, var, exp):
		self.var = var
		self.exp = exp
	
	def __repr__(self):
		return "Assign({0}, {1})".format(repr(self.var), repr(self.exp))
	
	def getChildren(self):
		return [self.exp]
	
	def toGraph(self):
		pass
	
	def toPython(self):
		return "{0} = {1}".format(self.var.toPython(), self.exp.toPython())

class FunctionCall(Statement):
	def __init__(self, name, args):
		self.name = name
		self.args = args
	
	def __repr__(self):
		return "FunctionCall({0}, {1})".format(repr(self.name), repr(self.args))
	
	def getChildren(self):
		return self.args
	
	def toGraph(self):
		pass
	
	def toPython(self):
		call = self.name.toPython() + "("
		
		for arg in self.args:
			call += arg.toPython() + ", "
		
		if len(self.args) > 0:
			call = call[0:-2]
		
		return call + ")"

class Expression(Node):
	pass

class Name(Expression):
	def __init__(self, name):
		self.name = name
	
	def __repr__(self):
		return "Name({0})".format(repr(self.name))
	
	def getChildren(self):
		return []
	
	def isSimple(self):
		return True
	
	def toGraph(self):
		pass
	
	def toPython(self):
		return self.name

class Integer(Expression):
	def __init__(self, value):
		self.value = value
	
	def __repr__(self):
		return "Integer({0:d})".format(self.value)
	
	def __str__(self):
		return "${0:d}".format(self.value)
	
	def getChildren(self):
		return []
	
	def isSimple(self):
		return True
	
	def toGraph(self):
		pass
	
	def toPython(self):
		return "{0:d}".format(self.value)

class BinOp(Expression):
	def __init__(self, operator, left, right):
		self.operator = operator
		self.left = left
		self.right = right
	
	def getChildren(self):
		return [self.left, self.right]
	
	def toGraph(self):
		pass
	
	def toPython(self):
		return "{0} {1} {2}".format(self.left.toPython(), self.operator, self.right.toPython())

class UnaryOp(Expression):
	def __init__(self, operator, operand):
		self.operator = operator
		self.operand = operand
	
	def getChildren(self):
		return [self.operand]
	
	def toGraph(self):
		pass
	
	def toPython(self):
		return "{0}{1}".format(self.operator, self.operand.toPython())

class Negate(UnaryOp):
	def __init__(self, operand):
		self.operator = '-'
		self.operand = operand
	
	def __repr__(self):
		return "Negate({0})".format(repr(self.operand))
	
	def opInstr(self):
		return "neg"

class Add(BinOp):
	def __init__(self, left, right):
		self.operator = '+'
		self.left = left
		self.right = right
	
	def __repr__(self):
		return "Add({0}, {1})".format(repr(self.left), repr(self.right))
	
	def opInstr(self):
		return "add"

class Div(BinOp):
	def __init__(self, left, right):
		self.operator = '/'
		self.left = left
		self.right = right
	
	def __repr__(self):
		return "Div({0}, {1})".format(repr(self.left), repr(self.right))
	
	def opInstr(self):
		return "idiv"

class Mul(BinOp):
	def __init__(self, left, right):
		self.operator = '*'
		self.left = left
		self.right = right
	
	def __repr__(self):
		return "Mul({0}, {1})".format(repr(self.left), repr(self.right))
	
	def opInstr(self):
		return "imul"

class Sub(BinOp):
	def __init__(self, left, right):
		self.operator = '-'
		self.left = left
		self.right = right
	
	def __repr__(self):
		return "Sub({0}, {1})".format(repr(self.left), repr(self.right))
	
	def opInstr(self):
		return "sub"
