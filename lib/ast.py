"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/08/23
Description:	Describes the abstract syntax tree used by my compiler for HW0.
"""

from util import *

##############
# Base Class #
##############

class Node(dict):
	def __iter__(self):
		for n in self.getChildren():
			yield n
	
	def collectSymbols(self, which = 'b'):
		symbols = set([])
		
		for n in self:
			symbols |= n.collectSymbols(which)
		
		return symbols
	
	def getChildren(self):
		return []
	
	def isSimple(self):
		return True
	
	def setChildren(self, children):
		pass

###############
# SSA Classes #
###############

class Phi(Node):
	def __init__(self, target, *srcs):
		self.target = target
		self.srcs = list(srcs)
	
	def __repr__(self):
		return 'Phi(' + repr(self.target) + ', ' + repr(self.srcs) + ')'
	
	def addSrc(self, src):
		self.srcs.append(src)
	
	def collectSymbols(self, which):
		syms = set([])
		
		if which != 'r':
			syms |= set([self.target])
		
		if which != 'w':
			syms |= set(self.srcs)
		
		return syms
	
	def getChildren(self):
		return self.srcs
	
	def setChildren(self, children):
		self.srcs = children
	
	def toPython(self, level = 0):
		ret  = pad(level)
		ret += self.target.toPython()
		ret += ' = Phi('
		ret += ', '.join(map(lambda sym: str(sym), self.srcs))
		ret += ")\n"
		
		return ret

class Join(Node):
	def __init__(self):
		self.phis = []
	
	def __repr__(self):
		return 'Join(' + repr(self.phis) + ')'
	
	def addSymbol(self, sym, st = None):
		phi0 = None
		
		for phi1 in self.phis:
			if phi1.target.name == sym.name:
				phi0 = phi1
				break
		
		if phi0 != None:
			if sym != phi0.target and sym not in phi0.srcs:
				phi0.addSrc(sym)
			
			else:
				return sym
		
		elif st != None:
			target = st.getSymbol(sym.name, True)
			phi0 = Phi(target, sym)
			self.phis.append(phi0)
		
		return phi0.target
	
	def getChildren(self):
		return self.phis
	
	def getTargets(self):
		return [phi.target for phi in self.phis]
	
	def setChildren(self, children):
		self.phis = children
	
	def toPython(self, level = 0):
		ret = ''
		
		for phi in self.phis:
			ret += phi.toPython(level)
		
		return ret

class BasicBlock(Node):
	def __init__(self, children):
		self.children = children
	
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

class Class(Node):
	def __init__(self, name, bases, body):
		self.name = name
		self.bases = bases
		self.body = body
	
	def __repr__(self):
		return "Class({0}, Bases: {1}, Body: {2}".format(repr(self.name), repr(self.bases), repr(self.body))
	
	def getChildren(self):
		tmp = [self.name] + self.bases + [self.body]
		
		return tmp
	
	def isSimple(self):
		return False
	
	def setChildren(self, children):
		self.name = children[0]
		self.bases = children[1:-1] if len(children) > 2 else []
		self.body = children[-1]
	
	def toPython(self, level = 0):
		ret  = pad(level)
		ret += "class {0}({1}):\n".format(self.name, [base.toPthon() for base in self.bases])
		ret += self.body.toPython(level + 1)
		
		return ret

class Function(Node):
	def __init__(self, name, argSymbols, block, st, migrated = False):
		self.name = name
		self.argSymbols = argSymbols
		self.block = block
		self.st = st
	
	def __repr__(self):
		return "Function({0}, {1}, {2})".format(repr(self.name), repr(self.argSymbols), repr(self.block))
	
	def collectSymbols(self, which = 'b'):
		syms = self.block.collectSymbols(which)
		
		if which == 'b' or which == 'w':
			syms |= set(self.argSymbols)
		
		return syms
	
	def getChildren(self):
		return [self.block]
	
	def setChildren(self, children):
		self.block = children[-1]
	
	def toPython(self, level = 0):
		argNames = ', '.join(map(lambda sym: str(sym), self.argSymbols))
		
		ret  = pad(level) + "def {0}({1}):\n".format(self.name, argNames)
		ret += self.block.toPython(level + 1)
		
		return ret

class Module(Node):
	def __init__(self, functions, strings):
		self.functions = functions
		self.strings = strings
	
	def __repr__(self):
		return "Module({0}, Strings: {1})".format(repr(self.functions), repr(self.strings))
	
	def getChildren(self):
		return self.functions
	
	def setChildren(self, children):
		self.functions = children
	
	def toPython(self, level = 0):
		ret = ""
		
		for fun in self.functions:
			ret += fun.toPython() + "\n"
		
		return ret

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
	
	def collectSymbols(self, which):
		syms = self.exp.collectSymbols(which)
		
		if which != 'r':
			syms |= set([self.var])
		
		return syms
	
	def getChildren(self):
		return [self.exp]
	
	def setChildren(self, children):
		self.exp = children[0]
	
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
	
	def toPython(self, level = 0):
		ret  = pad(level)
		ret += "if {0}:\n".format(self.cond.toPython())
		ret += self.then.toPython(level + 1)
		ret += pad(level)
		ret += "else:\n"
		ret += self.els.toPython(level + 1)
		ret += "\n"
		ret += self.jn.toPython(level)
		
		return ret

class Return(Statement):
	def __init__(self, value):
		self.value = value
	
	def __repr__(self):
		return "Return({0})".format(repr(self.value))
	
	def getChildren(self):
		return [self.value]
	
	def setChildren(self, children):
		self.value = children[0]
	
	def toPython(self, level = 0):
		return pad(level) + 'return ' + self.value.toPython()

class While(Statement):
	def __init__(self, cond, body, jn):
		self.cond	= cond
		self.body	= body
		self.jn	= jn
		
		self.condBody = BasicBlock([])
	
	def __repr__(self):
		return "While(Cond: {0}, CondBody: {1}, Body: {2}, Join: {3})".format(self.cond, self.condBody, self.body, self.jn)
	
	def getChildren(self):
		return [self.cond, self.condBody, self.body, self.jn]
	
	def setChildren(self, children):
		self.cond		= children[0]
		self.condBody	= children[1]
		self.body		= children[2]
		self.jn		= children[3]
	
	def toPython(self, level = 0):
		ret  = pad(level)
		ret += "while:\n"
		
		ret += pad(level + 1)
		ret += "Cond:\n"
		ret += pad(level + 2)
		ret += self.cond.toPython(level + 2)
		ret += "\n"
		
		ret += pad(level + 1)
		ret += "CondBody:\n"
		ret += self.condBody.toPython(level + 2)
		
		ret += pad(level + 1)
		ret += "Body:\n"
		ret += self.body.toPython(level + 2)
		
		ret += pad(level + 1)
		ret += "Join:\n"
		ret += self.jn.toPython(level + 2)
		
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
	
	def isSimple(self):
		return False
	
	def setChildren(self, children):
		self.cond = children[0]
		self.then = children[1]
		self.els  = children[2]
	
	def toPython(self, level = 0):
		ret  = pad(level)
		ret += "if {0}:\n".format(self.cond.toPython())
		ret += self.then.toPython(level + 1)
		ret += pad(level)
		ret += "else:\n"
		ret += self.els.toPython(level + 1)
		
		return ret

class FunctionCall(Expression):
	def __init__(self, name, *args):
		self.name = name
		self.args = list(args)
		self.tag = False
	
	def __repr__(self):
		return "FunctionCall({0}, {1})".format(repr(self.name), self.args)
	
	def getChildren(self):
		return [self.name] + self.args
	
	def setChildren(self, children):
		self.name = children[0]
		self.args = children[1:]
	
	def toPython(self, level = 0):
		ret  = pad(level)
		ret += self.name.toPython() + '('
		
		for arg in self.args:
			ret += arg.toPython() + ', '
		
		if len(self.args) > 0:
			ret = ret[0:-2]
		
		return ret + ')'

class GetAttr(Expression):
	def __init__(self, exp, attrName):
		self.exp = exp
		self.attrName = attrName
	
	def __repr__(self):
		return "GetAttr({0}, {1}".format(repr(self.exp), repr(self.attrName))
	
	def getChildren(self):
		return [self.exp, self.attrName]
	
	def setChildren(self, children):
		self.exp = children[0]
		self.attrName = children[1]
	
	def toPython(self, level = 0):
		return self.exp.toPython() + '.' + self.attrName.toPython()

class SetAttr(Expression):
	def __init__(self, exp, attrName, value):
		self.exp = exp
		self.attrName = attrName
		self.value = value
	
	def __repr__(self):
		return "SetAttr({0}, {1}, {2})".format(self.exp, self.attrName, self.value)
	
	def getChildren(self):
		return [self.exp, self.attrName, self.value]
	
	def setChildren(self, children):
		self.exp = children[0]
		self.attrName = children[1]
		self.value = children[2]
	
	def toPython(self, level = 0):
		return "{0}.{1} = {2}".format(*[child.toPython(level) for child in node])

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
		ret += "({0} {1} {2})".format(self.left.toPython(), self.operator, self.right.toPython())
		
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

class Literal(Expression):
	pass

class Boolean(Value, Literal):
	def __repr__(self):
		return str(self)
	
	def toPython(self, level = 0):
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

class Dictionary(Value, Literal):
	def __init__(self, pairs):
		self.value = pairs
	
	def __hash__(self):
		return hash(self.pairs)
	
	def __repr__(self):
		return "Dictionary({0})".format(repr(self.value))
	
	def __str__(self):
		return str(self.value)
	
	def getChildren(self):
		return self.value.keys() + self.value.values()
	
	def isSimple(self):
		return False
	
	def setChildren(self, children):
		newPairs = {}
		
		keyLen = len(children) / 2
		
		for index in range(0, keyLen):
			newPairs[children[index]] = children[index + keyLen]
		
		self.value = newPairs
	
	def toPython(self, level = 0):
		pairs = []
		
		for key in self.value:
			pairs.append("{0}:{1}".format(key.toPython(), self.value[key].toPython()))
		
		return pad(level) + '{' + ', '.join(pairs) + '}'

class Integer(Value, Literal):
	def __init__(self, value):
		self.value = value
	
	def __hash__(self):
		return hash(self.value)
	
	def __repr__(self):
		return "Integer({0:d})".format(self.value)
	
	def __str__(self):
		return "${0:d}".format(self.value)
	
	def toPython(self, level = 0):
		return "{0:d}".format(self.value)

class List(Value, Literal):
	def __init__(self, elements):
		self.value = elements
	
	def __hash__(self):
		return hash(self.value)
	
	def __repr__(self):
		return "List({0})".format(repr(self.value))
	
	def __str__(self):
		return str(self.value)
	
	def getChildren(self):
		return self.value
	
	def isSimple(self):
		return False
	
	def setChildren(self, children):
		self.value = children
	
	def toPython(self, level = 0):
		els = []
		
		for child in self:
			els.append(child.toPython())
		
		return pad(level) + '[' + ', '.join(els) + ']'

class Name(Value):
	def __init__(self, name, version = -1):
		self.name = name
		self.version = version
	
	def __hash__(self):
		return hash(self.name)
	
	def __repr__(self):
		return "Name({0})".format(self.name) if self.version == -1 else "Name({0}:{1})".format(self.name, self.version)
	
	def __str__(self):
		return self.name if self.version == -1 else "__{0}_{1}".format(self.name, self.version)
	
	def toPython(self, level = 0):
		return str(self)

class String(Value):
	def __init__(self, value):
		self.value = value
	
	def __hash__(self):
		hash(self.value)
	
	def __repr__(self):
		return "String({0})".format(self.value)
	
	def __str__(self):
		return "'{0}'".format(self.value)
	
	def toPython(self, level = 0):
		return str(self)

class Symbol(Value):
	def __init__(self, name, version):
		self.name = name
		self.version = version
	
	def __eq__(self, other):
		if isinstance(other, Symbol):
			return self.name == other.name and self.version == other.version
		else:
			return False
	
	def __hash__(self):
		return id(self)
	
	def __ne__(self, other):
		if isinstance(other, Symbol):
			return self.name != other.name or self.version != other.version
		else:
			return True
	
	def __repr__(self):
		return "Symbol({0})".format(self)
	
	def __str__(self):
		return "{0}:{1:d}".format(self.name, self.version)
	
	def collectSymbols(self, which = 'b'):
		return set([self]) if which != 'w' else set([])
	
	def toPython(self, level = 0):
		return str(self)

class Subscript(Value):
	def __init__(self, symbol, subscript):
		self.symbol = symbol
		self.subscript = subscript
	
	def __hash__(self):
		return hash(str(self.symbol) + str(self.subscript))
	
	def __repr__(self):
		return "Subscript({0}, {1})".format(repr(self.symbol), repr(self.subscript))
	
	def __str__(self):
		return "{0}[{1}]".format(self.symbol, self.subscript)
	
	def getChildren(self):
		return [self.symbol, self.subscript]
	
	def isSimple(self):
		return False
	
	def setChildren(self, children):
		self.symbol = children[0]
		self.subscript = children[1]
	
	def toPython(self, level = 0):
		return pad(level) + str(self)
