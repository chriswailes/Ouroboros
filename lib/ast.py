"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/08/23
Description:	Describes the abstract syntax tree used by my compiler for HW0.
"""

from util import *

from symbol_table import SymbolTable

##############
# Base Class #
##############

class Node(dict):
	def __iter__(self):
		for n in self.getChildren():
			yield n
	
	def collectSymbols(self):
		symbols = set([])
		
		for n in self:
			symbols |= n.collectSymbols()
		
		return symbols
	
	def getChildren(self):
		return []
	
	def setChildren(self, children):
		pass

###############
# SSA Classes #
###############

class Phi(Node):
	def __init__(self, target, srcs = []):
		self.target = target
		self.srcs = srcs
	
	def __repr__(self):
		return 'Phi(' + repr(self.target) + ', ' + repr(self.srcs) + ')'
	
	def addSrc(self, src):
		self.srcs.append(src)
	
	def getChildren(self):
		return self.srcs
	
	def setChildren(self, children):
		self.srcs = children

class Join(Node):
	def __init__(self):
		self.phis = []
	
	def __repr__(self):
		return 'Join(' + repr(self.phis) + ')'
	
	def addName(self, name, st = None):
		phi0 = None
		
		for phi1 in self.phis:
			if phi1.target.symbol.name == name.symbol.name:
				phi0 = phi1
				break
		
		if phi0 != None:
			phi0.addSrc(name)
		
		elif st != None:
			target = Name(st.getSymbol(name.symbol.name, True))
			phi0 = Phi(target, [name])
			self.phis.append(phi0)
	
	def getChildren(self):
		return self.phis
	
	def getTargets(self):
		targets = []
		
		for phi in self.phis:
			targets.append(phi.target)
		
		return targets
	
	def setChildren(self, children):
		self.phis = children

class BasicBlock(Node):
	def __init__(self, children, st = SymbolTable()):
		self.children = children
		self.st = st
	
	def __repr__(self):
		return 'BasicBlock(' + repr(self.children) + ')'
	
	def getChildren(self):
		return self.children
	
	def setChildren(self, children):
		self.children = children
	
	def toPython(self, level = 0):
		ret = ''
		
		for node in self.children:
			ret += node.toPython(level) + "\n"
		
		return ret

##############################
# Modules, Defs, and Classes #
##############################

class Module(Node):
	def __init__(self, block):
		self.block = block
	
	def __repr__(self):
		return "Module({0})".format(repr(self.block))
	
	def getChildren(self):
		return [self.block]
	
	def setChildren(self, children):
		self.block = children[0]
	
	def toGraph(self):
		pass
	
	def toPython(self):
		return self.block.toPython()

##############
# Statements #
##############

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
	
	def setChildren(self, children):
		self.exp = children[0]
	
	def toGraph(self):
		pass
	
	def toPython(self, level = 0):
		ret  = pad(level)
		ret += "{0} = {1}".format(self.var.toPython(), self.exp.toPython())
		
		return ret

class If(Statement):
	def __init__(self, cond, then, els, jn):
		self.cond = cond
		self.jn = jn
		
		if isinstance(then, BasicBlock) and isinstance(els, BasicBlock):
			self.then = then
			self.els  = els
		else:
			raise Exception("Not a basic block.")
	
	def __repr__(self):
		return "If(Cond: {0}, Then: {1}, Else: {2}, Join: {3})".format(repr(self.cond), repr(self.then), repr(self.els), repr(self.jn))
	
	def getChildren(self):
		return [self.cond, self.then, self.els, self.jn]
	
	def setChildren(self, children):
		self.cond = children[0]
		self.then = children[1]
		self.els  = children[2]
		self.jn	= children[3]
	
	def toGraph(self):
		pass
	
	def toPython(self, level = 0):
		ret  = pad(level)
		ret += "if {0}:\n".format(self.cond.toPython())
		ret += self.then.toPython(level + 1)
		ret += pad(level)
		ret += "else:\n"
		ret += self.els.toPython(level + 1)
		
		return ret

###############
# Expressions #
###############

class Expression(Node):
	pass

class IfExp(Expression):
	def __init__(self, cond, then, els):
		self.cond = cond
		self.then = then
		self.els = els
	
	def __repr__(self):
		return "IfExp(Cond: {0}, Then: {1}, Else: {2})".format(repr(self.cond), repr(self.then), repr(self.els))
	
	def getChildren(self):
		return [self.cond, self.then, self.els]
	
	def setChildren(self, children):
		self.cond = children[0]
		self.then = children[1]
		self.els  = children[2]
	
	def toGraph(self):
		pass
	
	def toPython(self, level = 0):
		ret  = pad(level)
		ret += "if {0}:\n".format(self.cond.toPython())
		ret += self.then.toPython(level + 1)
		ret += pad(level)
		ret += "else:\n"
		ret += self.els.toPython(level + 1)
		
		return ret

class FunctionCall(Expression):
	def __init__(self, name, args = []):
		self.name = name
		self.args = args
	
	def __repr__(self):
		return "FunctionCall({0}, {1})".format(repr(self.name), repr(self.args))
	
	def getChildren(self):
		return self.args
	
	def toGraph(self):
		pass
	
	def setChildren(self, children):
		self.args = children
	
	def toPython(self, level = 0):
		ret  = pad(level)
		ret += self.name.toPython() + '('
		
		for arg in self.args:
			ret += arg.toPython() + ', '
		
		if len(self.args) > 0:
			ret = ret[0:-2]
		
		return ret + ')'

class BinOp(Expression):
	def __init__(self, operator, left, right):
		self.operator = operator
		self.left = left
		self.right = right
	
	def __repr__(self):
		return "{0}({1}, {2})".format(self.__class__.__name__, repr(self.left), repr(self.right))
	
	def getChildren(self):
		return [self.left, self.right]
	
	def setChildren(self, children):
		self.left  = children[0]
		self.right = children[1]
	
	def toGraph(self):
		pass
	
	def toPython(self, level = 0):
		ret  = pad(level)
		ret += "{0} {1} {2}".format(self.left.toPython(), self.operator, self.right.toPython())
		
		return ret

class UnaryOp(Expression):
	def __init__(self, operator, operand):
		self.operator = operator
		self.operand = operand
	
	def __repr__(self):
		return "{0}({1})".format(self.__class__.__name__, repr(self.operand))
	
	def getChildren(self):
		return [self.operand]
	
	def setChildren(self, children):
		self.operand = children[0]
	
	def toGraph(self):
		pass
	
	def toPython(self, level = 0):
		ret  = pad(level)
		ret += "{0}({1})".format(self.operator, self.operand.toPython())
		
		return ret

class Arithmatic(Expression):
	pass

class Logical(Expression):
	pass

###################
# Unary Operators #
###################

class Negate(UnaryOp, Arithmatic):
	def __init__(self, operand):
		super(Negate, self).__init__('-', operand)

class Not(UnaryOp, Logical):
	def __init__(self, operand):
		super(Not, self).__init__('not ', operand)

####################
# Binary Operators #
####################

class Add(BinOp, Arithmatic):
	def __init__(self, left, right):
		super(Add, self).__init__('+', left, right)

class And(BinOp, Logical):
	def __init__(self, left, right):
		super(And, self).__init__('and', left, right)

class Eq(BinOp, Logical):
	def __init__(self, left, right):
		super(Eq, self).__init__('==', left, right)

class Div(BinOp, Arithmatic):
	def __init__(self, left, right):
		super(Div, self).__init__('/', left, right)

class Is(BinOp, Logical):
	def __init__(self, left, right):
		super(Is, self).__init__('is', left, right)

class Mul(BinOp, Arithmatic):
	def __init__(self, left, right):
		super(Mul, self).__init__('*', left, right)

class Ne(BinOp, Logical):
	def __init__(self, left, right):
		super(Ne, self).__init__('!=', left, right)

class Or(BinOp, Logical):
	def __init__(self, left, right):
		super(Or, self).__init__('or', left, right)

class Sub(BinOp, Arithmatic):
	def __init__(self, left, right):
		super(Sub, self).__init__('-', left, right)

##########
# Values #
##########

class Value(Expression):
	pass

class Boolean(Value):
	def __repr__(self):
		return str(self)
	
	def toPython(self):
		return str(self)

class Fals(Boolean):
	def __init__(self):
		self.value = False
	
	def __str__(self):
		return 'False'

class Tru(Boolean):
	def __init__(self):
		self.value = True
	
	def __str__(self):
		return 'True'

class Dictionary(Value):
	def __init__(self, pairs):
		self.value = self.pairs = pairs
	
	def __hash__(self):
		return hash(self.pairs)
	
	def __repr__(self):
		return "Dictionary({0})".format(repr(self.pairs))
	
	def __str__(self):
		return str(self.pairs)
	
	def getChildren(self):
		return self.pairs.keys() + self.pairs.values()
	
	def setChildren(self, children):
		newPairs = {}
		
		keyLen = len(children) / 2
		
		for index in range(0, keyLen):
			newPairs[children[index]] = children[index + keyLen]
		
		self.pairs = newPairs
	
	def toPython(self, level = 0):
		pairs = []
		
		for key in self.pairs:
			pairs.append("{0}:{1}".format(key.toPython(), self.pairs[key].toPython()))
		
		return pad(level) + '{' + ', '.join(pairs) + '}'

class Integer(Value):
	def __init__(self, value):
		self.value = value
	
	def __hash__(self):
		return hash(self.value)
	
	def __repr__(self):
		return "Integer({0:d})".format(self.value)
	
	def __str__(self):
		return "${0:d}".format(self.value)
	
	def toGraph(self):
		pass
	
	def toPython(self, level = 0):
		return "{0:d}".format(self.value)

class List(Value):
	def __init__(self, elements):
		self.value = self.elements = elements
	
	def __hash__(self):
		return hash(self.elements)
	
	def __repr__(self):
		return "List({0})".format(repr(self.elements))
	
	def __str__(self):
		return str(self.elements)
	
	def getChildren(self):
		return self.elements
	
	def setChildren(self, children):
		self.elements = children
	
	def toPython(self, level = 0):
		els = []
		
		for child in self:
			els.append(child.toPython())
		
		return pad(level) + '[' + ', '.join(els) + ']'

class Name(Value):
	def __init__(self, symbol):
		self.symbol = symbol
	
	def __hash__(self):
		return hash(self.symbol)
	
	def __repr__(self):
		return "Name({0})".format(str(self.symbol))
	
	def __str__(self):
		return str(self.symbol)
	
	def collectSymbols(self):
		return set([self.symbol])
	
	def toGraph(self):
		pass
	
	def toPython(self, level = 0):
		return str(self.symbol)

class Subscript(Value):
	def __init__(self, name, subscript):
		self.name = name
		self.subscript = subscript
	
	def __hash__(self):
		return hash(str(self.name) + str(self.subcript))
	
	def __repr__(self):
		return "Subscript({0}, {1})".format(repr(self.name), repr(self.subscript))
	
	def __str__(self):
		return "{0}[{1}]".format(self.name, self.subscript.value)
	
	def getChildren(self):
		return [self.subscript]
	
	def setChildren(self, children):
		self.subscript = children[0]
	
	def toPython(self, level = 0):
		return pad(level) + str(self)
