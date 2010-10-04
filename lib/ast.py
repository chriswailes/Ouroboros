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
	
	def isSimple(self):
		return False

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

class Join(Node):
	def __init__(self):
		self.phis = []
	
	def __repr__(self):
		return 'Join(' + repr(self.phis) + ')'
	
	def addSymbol(self, symbol, st = None):
		phi0 = None
		
		for phi1 in self.phis:
			if phi1.target.name == symbol.name:
				phi0 = phi1
				break
		
		if phi0:
			phi0.addSrc(symbol)
		elif st:
			target = st.getSymbol(symbol.name, True)
			phi0 = Phi(target, [symbol])
			self.phis.append(phi0)
	
	def getTargets(self):
		targets = []
		
		for phi in self.phis:
			targets.append(phi.target)
		
		return targets

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

###############
# Expressions #
###############

class Expression(Node):
	pass

class FunctionCall(Expression):
	def __init__(self, name, args):
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

class Negate(UnaryOp):
	def __init__(self, operand):
		super(UnaryOp, self).__init__('-', operand)

class Not(UnaryOp):
	def __init__(self, operand):
		super(UnaryOp, self).__init__('not ', operand)

class Add(BinOp):
	def __init__(self, left, right):
		super(BinOp, self).__init__('+', left, right)

class And(BinOp):
	def __init__(self, left, right):
		super(BinOp, self).__init__('and', left, right)

class Eq(BinOp):
	def __init__(self, left, right):
		super(BinOp, self).__init__('==', left, right)

class Div(BinOp):
	def __init__(self, left, right):
		super(BinOp, self).__init__('/', left, right)

class Mul(BinOp):
	def __init__(self, left, right):
		super(BinOp, self).__init__('*', left, right)

class Ne(BinOp):
	def __init__(self, left, right):
		super(BinOp, self).__init__('!=', left, right)

class Or(BinOp):
	def __init__(self, left, right):
		super(BinOp, self).__init__('or', left, right)

class Sub(BinOp):
	def __init__(self, left, right):
		super(BinOp, self).__init__('-', left, right)

##########
# Values #
##########

class Value(Expression):
	pass

class Boolean(Value):
	pass

class Fals(Boolean):
	pass

class Tru(Boolean):
	pass

class Dictionary(Value):
	def __init__(self, pairs):
		self.pairs = pairs
	
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
		pythonPairs = {}
		
		for key in self:
			pythonPairs[key.toPython()] = self.pairs[key].toPython()
		
		return pad(level) + str(els)

class Integer(Value):
	def __init__(self, value):
		self.value = value
	
	def __hash__(self):
		return hash(self.value)
	
	def __repr__(self):
		return "Integer({0:d})".format(self.value)
	
	def __str__(self):
		return "${0:d}".format(self.value)
	
	def isSimple(self):
		return True
	
	def toGraph(self):
		pass
	
	def toPython(self, level = 0):
		return "{0:d}".format(self.value)

class List(Value):
	def __init__(self, elements):
		self.elements = elements
	
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
		
		return pad(level) + str(els)

class Name(Value):
	def __init__(self, symbol):
		self.symbol = symbol
	
	def __hash__(self):
		return hash(symbol)
	
	def __repr__(self):
		return "Name({0})".format(str(self.symbol))
	
	def __str__(self):
		return str(self.symbol)
	
	def isSimple(self):
		return True
	
	def collectSymbols(self):
		return set([self.symbol])
	
	def toGraph(self):
		pass
	
	def toPython(self, level = 0):
		return str(self.symbol)

class Subscript(Value):
	def __init__(self, symbol, subscript):
		self.symbol = symbol
		self.subscript = subscript
	
	def __hash__(self):
		return hash(str(sym) + str(subcript))
	
	def __repr__(self):
		return "Subscript({0}, {1})".format(repr(self.symbol), repr(self.subscript))
	
	def __str__(self):
		return "{0}[{1}]".format(self.symbol, self.subscript)
	
	def getChildren(self):
		return [self.symbol, self.subscript]
	
	def setChildren(self, children):
		self.symbol = children[0]
		self.subscript = children[1]
	
	def toPython(self, level = 0):
		return pad(level) + str(self)
