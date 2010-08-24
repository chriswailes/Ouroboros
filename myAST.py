"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW0
Date:		2010/08/23
Description:	Describes the abstract syntax tree used by my compiler for HW0.
"""

import compiler
import compiler.ast as ast

stackSize = 0
def getStackSize():
	global stackSize
	
	return stackSize

varNum = 0
varLocs = {}
def getVar():
	global varNum
	global varLocs
	
	global stackSize
	
	var = Name("tmp%d" % (varNum))
	
	varLocs[var] = varNum * 4
	varNum += 1
	
	stackSize += 4
	
	return var

def getVarLoc(var):
	global varLocs
	
	return varLocs[var]

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

def toMyAST(oldAST):
	if isinstance(oldAST, ast.Add):
		left = toMyAST(oldAST.left)
		right = toMyAST(oldAST.right)
		
		return Add(left, right)
	
	elif isinstance(oldAST, ast.Assign):
		name = toMyAST(oldAST.nodes.pop())
		expr = toMyAST(oldAST.expr)
		
		return Assign(name, expr)
	
	elif isinstance(oldAST, ast.AssName):
		return Name(oldAST.name)
	
	elif isinstance(oldAST, ast.CallFunc):
		name = toMyAST(oldAST.node)
		args = [toMyAST for a in oldAST.args]
		
		return FunctionCall(name, args)
	
	elif isinstance(oldAST, ast.Const):
		return Integer(oldAST.value)
	
	elif isinstance(oldAST, ast.Discard):
		return toMyAST(oldAST.expr)
		
	elif isinstance(oldAST, ast.Module):
		children = flatten([toMyAST(n) for n in oldAST.getChildNodes()])
		
		return Module(children)
	
	elif isinstance(oldAST, ast.Name):
		return Name(oldAST.name)
		
	elif isinstance(oldAST, ast.Printnl):
		children = flatten([toMyAST(e) for e in oldAST.getChildNodes()])
		
		return Print(children)
		
	elif isinstance(oldAST, ast.Stmt):
		stmts = flatten([toMyAST(s) for s in oldAST.getChildNodes()])
		
		return stmts
		
	elif isinstance(oldAST, ast.UnarySub):
		operand = toMyAST(oldAST.expr)
		
		return Negate(operand)
	
	else:
		None
	

class Node:
	def __iter__(self):
		for n in self.getChildren():
			yield n
	
	def compile(self):
		pass
	
	def flatten(self):
		pass
	
	def getAttr(self, key):
		return self.attributes[key]
	
	def getChildren(self):
		pass
	
	def isSimple(self):
		False
	
	def setAttr(self, key, value):
		self.attributes[key] = value
	
	def toGraph(self):
		pass
	
	def toPython(self):
		pass

class Module(Node):
	def __init__(self, stmts):
		self.stmts = stmts
	
	def __repr__(self):
		return "Module(%s)" % (repr(self.stmts))
	
	def compile(self):
		subCode = ""
		
		code  = ".globl main\n"
		code += "main:\n"
		code += "\tpushl %ebp\n"
		
		for stmt in self.stmts:
			tmpSubCode, foo = stmt.compile()
			
			subCode += tmpSubCode + "\n"
		
		code += "\tsubl $%d, %%esp\n\n" % (getStackSize())
		
		code += subCode
		
		return code
	
	def flatten(self):
		newStmts = []
		
		for s in self.stmts:
			preStmts, newStmt = s.flatten()
			
			newStmts.append(preStmts)
			newStmts.append(newStmt)
		
		self.stmts = flatten(newStmts)
		return self
	
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
	def compile(self):
		pass
	
	def flatten(self):
		pass
	
	def getChildren(self):
		pass
	
	def toGraph(self):
		pass
	
	def toPython(self):
		pass

class Assign(Node):
	def __init__(self, var, exp):
		self.var = var
		self.exp = exp
	
	def __repr__(self):
		return "Assignment(%s, %s)" % (repr(self.var), repr(self.exp))
	
	def compile(self):
		pass
		
		"""
		code, subResult = self.exp.compile()
		
		result = getVarLoc(self.var)
		
		code += "\tmovl -%d(%%ebp), %%eax\n" % (subResult)
		code += "\tmovl %%eax, -%d(%%ebp)\n" % (result)
		
		code += "\n"
		
		return code, self.var
		"""
	
	def flatten(self):
		preStmts, self.exp = self.exp.flatten()
		
		return preStmts, self
	
	def getChildren(self):
		return [self.exp]
	
	def toGraph(self):
		pass
	
	def toPython(self):
		return "%s = %s" % (self.var.toPython(), self.exp.toPython())

class FunctionCall(Statement):
	def __init__(self, name, args):
		self.name = name
		self.args = args
	
	def __repr__(self):
		return "FunctionCall(%s, %s)" % (repr(self.name), repr(self.args))
	
	def compile(self):
		pass
	
	def flatten(self):
		preStmts = []
		newArgs = []
		
		for arg in self.args:
			tmpPreStmts, newArg = arg.flatten
			
			preStmts.append(tmpPreStmts)
			newArgs.append(newArg)
		
		preStmts = flatten(preStmts)
		self.args = newArgs
		
		var = getVar()
		preStmts.append(Assign(var, self))
		
		return preStmts, var
	
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

class Print(Statement):
	def __init__(self, exps):
		self.exps = exps
	
	def __repr__(self):
		return "Print(%s)" % (repr(self.exps))
	
	def flatten(self):
		preStmts = []
		newExps = []
		
		for exp in self.exps:
			subPreStmts, newExp = exp.flatten()
			
			preStmts.append(subPreStmts)
			newExps.append(newExp)
		
		preStmts = flatten(preStmts)
		self.exps = newExps
		
		return preStmts, self
	
	def compile(self):
		pass
	
	def getChildren(self):
		return self.exprs
	
	def toGraph(self):
		pass
	
	def toPython(self):
		call = "print("
		
		for exp in self.exps:
			call += exp.toPython() + ", "
		
		if len(call) > 0:
			call = call[0:-2]
		
		return call + ")"

class Expression(Node):
	def compile(self):
		pass
	
	def getChildren(self):
		pass
	
	def toGraph(self):
		pass

class Name(Expression):
	def __init__(self, name):
		self.name = name
	
	def __repr__(self):
		return "Name(%s)" % (repr(self.name))
	
	def compile(self):
		return "-%d(%%ebp)" % (getVarLoc(self.name))
	
	def flatten(self):
		return [], self
	
	def getChildren(self):
		[]
	
	def isSimple(self):
		True
	
	def toGraph(self):
		pass
	
	def toPython(self):
		return self.name

class Integer(Expression):
	def __init__(self, value):
		self.value = value
	
	def __repr__(self):
		return "Integer(%d)" % (self.value)
	
	def compile(self):
		return "$%d" % (self.value)
	
	def flatten(self):
		return [], self
	
	def getChildren(self):
		None
	
	def isSimple(self):
		True
	
	def toGraph(self):
		pass
	
	def toPython(self):
		return "%s" % (self.value)

class BinOp(Expression):
	def __init__(self, left, right):
		self.left = left
		self.right = right
	
	def compile(self):
		pass
	
	def flatten(self):
		leftPreStmts, self.left = self.left.flatten()
		rightPreStmts, self.right = self.right.flatten()
		
		var = getVar()
		assign = Assign(var, self)
		
		preStmts = [leftPreStmts, rightPreStmts, assign]
		
		return preStmts, var
	
	def getChildren(self):
		return [self.left, self.right]
	
	def opString(self):
		pass
	
	def toGraph(self):
		pass
	
	def toPython(self):
		return "%s %s %s" % (self.left.toPython(), self.opString(), self.right.toPython())

class UnaryOp(Expression):
	def __init__(self, operand):
		self.operand = operand
	
	def compile(self):
		pass
	
	def flatten(self):
		preStmts, self.operand = self.operand.flatten()
		
		var = getVar()
		preStmts.append(Assign(var, self))
		
		return preStmts, var
	
	def getChildren(self):
		return [self.operand]
	
	def opString(self):
		pass
	
	def toGraph(self):
		pass
	
	def toPython(self):
		return "%s%s" % (self.opString(), self.operand.toPython())

class Negate(UnaryOp):
	def __repr__(self):
		return "Negate(%s)" % (repr(self.operand))
	
	def opString(self):
		return "-"

class Add(BinOp):
	def __repr__(self):
		return "Add((%s, %s))" % (repr(self.left), repr(self.right))
	
	def opString(self):
		return "+"

class Div(BinOp):
	def __repr__(self):
		return "Add((%s, %s))" % (repr(self.left), repr(self.right))
	
	def opString(self):
		return "/"

class Mul(BinOp):
	def __repr__(self):
		return "Mul((%s, %s))" % (repr(self.left), repr(self.right))
	
	def opString(self):
		return "*"

class Sub(BinOp):
	def __repr__(self):
		return "Sub((%s, %s))" % (repr(self.left), repr(self.right))
	
	def opString(self):
		return "-"
