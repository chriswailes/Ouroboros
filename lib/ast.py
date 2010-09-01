"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/08/23
Description:	Describes the abstract syntax tree used by my compiler for HW0.
"""

import compiler
import compiler.ast as oast

from assembler import ib

from lib import registers as r
from lib import util
from lib import variables as v

def toMyAST(oldAST, funcName = False):
	if isinstance(oldAST, oast.Add):
		left = toMyAST(oldAST.left)
		right = toMyAST(oldAST.right)
		
		return Add(left, right)
	
	elif isinstance(oldAST, oast.Assign):
		name = toMyAST(oldAST.nodes.pop())
		expr = toMyAST(oldAST.expr)
		
		return Assign(name, expr)
	
	elif isinstance(oldAST, oast.AssName):
		name = v.addUserVar(oldAST.name)
		return Name(name)
	
	elif isinstance(oldAST, oast.CallFunc):
		name = toMyAST(oldAST.node, True)
		args = [toMyAST for a in oldAST.args]
		
		return FunctionCall(name, args)
	
	elif isinstance(oldAST, oast.Const):
		return Integer(oldAST.value)
	
	elif isinstance(oldAST, oast.Discard):
		return toMyAST(oldAST.expr)
	
	elif isinstance(oldAST, oast.Div):
		left = toMyAST(oldAST.left)
		right = toMyAST(oldAST.right)
		
		return Div(left, right)
		
	elif isinstance(oldAST, oast.Module):
		children = util.flatten([toMyAST(n) for n in oldAST.getChildNodes()])
		
		return Module(children)
	
	elif isinstance(oldAST, oast.Mul):
		left = toMyAST(oldAST.left)
		right = toMyAST(oldAST.right)
		
		return Mul(left, right)
	
	elif isinstance(oldAST, oast.Name):
		name = oldAST.name
		if not funcName:
			name = v.addUserVar(oldAST.name)
		
		return Name(name)
		
	elif isinstance(oldAST, oast.Printnl):
		children = util.flatten([toMyAST(e) for e in oldAST.getChildNodes()])
		
		return Print(children)
		
	elif isinstance(oldAST, oast.Stmt):
		stmts = util.flatten([toMyAST(s) for s in oldAST.getChildNodes()])
		
		return stmts
	
	elif isinstance(oldAST, oast.Sub):
		left = toMyAST(oldAST.left)
		right = toMyAST(oldAST.right)
		
		return Sub(left, right)
		
	elif isinstance(oldAST, oast.UnarySub):
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
		return "Module({0})".format(repr(self.stmts))
	
	def compile(self, dest = None):
		subCode = ib.Block()
		
		code = ib.Block()
		code.header  = ".globl main\n"
		code.header += "main:\n"
		
		#Push the old base pointer onto the stack.
		code.append(ib.OneOp("push", "%ebp"))
		#Make the old stack pointer the new base pointer.
		code.append(ib.TwoOp("mov", "%esp", "%ebp"))
		
		for stmt in self.stmts:
			subCode.append(stmt.compile())
		
		#Expand the stack.
		code.append(ib.TwoOp("sub", "$" + str(v.getStackSize()), "%esp"))
		
		code.append(subCode)
		
		endBlock = ib.Block()
		#Put our exit value in %eax
		endBlock.append(ib.TwoOp("mov", "$0", "%eax"))
		#Restore the stack.
		endBlock.append(ib.Instruction("leave"))
		#Return
		endBlock.append(ib.Instruction("ret"))

		code.append(endBlock)
		
		return code
	
	def flatten(self):
		newStmts = []
		
		for s in self.stmts:
			preStmts, newStmt = s.flatten()
			
			newStmts.append(preStmts)
			newStmts.append(newStmt)
		
		self.stmts = util.flatten(newStmts)
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
	def compile(self, dest):
		pass
	
	def flatten(self, inplace = False):
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
		return "Assign({0}, {1})".format(repr(self.var), repr(self.exp))
	
	def compile(self, dest = None):
		if isinstance(self.exp, Name):
			code = ib.Block()
			
			reg = r.alloc()
			code.append(ib.TwoOp("mov", self.exp.compile(), reg))
			code.append(ib.TwoOp("mov", reg, self.var))
			
			r.free(reg)
			
			return code
		else:
			return self.exp.compile(self.var)
	
	def flatten(self, inplace = True):
		preStmts, self.exp = self.exp.flatten(True)
		
		return preStmts, self
	
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
	
	def compile(self, dest = None):
		code = ib.Block()
		code.append(ib.OneOp("call", self.name.name, None))
		
		if dest:
			code.append(ib.TwoOp("mov", "%eax", dest))

		return code
	
	def flatten(self, inplace = False):
		preStmts = []
		newArgs = []
		
		for arg in self.args:
			tmpPreStmts, newArg = arg.flatten(False)
			
			preStmts.append(tmpPreStmts)
			newArgs.append(newArg)
		
		preStmts = util.flatten(preStmts)
		self.args = newArgs
		
		if inplace:
			return preStmts, self
		else:
			var = v.getVar()
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
	def __init__(self, args):
		self.args = args
	
	def __repr__(self):
		return "Print({0})".format(repr(self.args))
	
	def compile(self, dest = None):
		code = ib.Block()
		code.append(ib.OneOp("push", self.args[0].compile()))
		code.append(ib.OneOp("call", "print_int_nl", None))
		code.append(ib.TwoOp("add", "$4", "%esp"))
		
		return code
	
	def flatten(self, inplace = False):
		preStmts = []
		newArgs = []
		
		for arg in self.args:
			tmpPreStmts, newArg = arg.flatten(False)
			
			preStmts.append(tmpPreStmts)
			newArgs.append(newArg)
		
		preStmts = util.flatten(preStmts)
		self.args = newArgs
		
		return preStmts, self
	
	def getChildren(self):
		return self.exprs
	
	def toGraph(self):
		pass
	
	def toPython(self):
		call = "print("
		
		for arg in self.args:
			call += arg.toPython() + ", "
		
		if len(call) > 0:
			call = call[0:-2]
		
		return call + ")"

class Expression(Node):
	def compile(self, dest):
		pass
	
	def getChildren(self):
		pass
	
	def toGraph(self):
		pass

class Name(Expression):
	def __init__(self, name):
		self.name = name
	
	def __str__(self):
		return self.compile()
	
	def __repr__(self):
		return "Name({0})".format(repr(self.name))
	
	def compile(self, dest = None):
		return "-{0:d}(%ebp)".format(v.getVarLoc(self.name))
	
	def flatten(self, inplace = False):
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
		return "Integer({0:d})".format(self.value)
	
	def __str__(self):
		return self.compile()

	def compile(self, dest = None):
		return "${0:d}".format(self.value)
	
	def flatten(self, inplace = False):
		return [], self
	
	def getChildren(self):
		[]
	
	def isSimple(self):
		True
	
	def toGraph(self):
		pass
	
	def toPython(self):
		return "{0:d}".format(self.value)

class BinOp(Expression):
	def __init__(self, left, right):
		self.left = left
		self.right = right
	
	def compile(self, dest = None):
		code = ib.Block()
		reg = r.alloc()

		if isinstance(self.left, Integer) and isinstance(self.right, Integer):
			value = Integer(eval("{0:d} {1} {2:d}".format(self.left.value, self.opString(), self.right.value)))
			code.append(ib.TwoOp("mov", value, dest))

		else:
			if isinstance(dest, Name):
				code.append(ib.TwoOp("mov", self.left, reg))
				code.append(ib.TwoOp(self.opInstr(), self.right, reg))
				code.append(ib.TwoOp("mov", reg, dest))
			else:
				#In this case the destination is a register.
				code.append(ib.TwoOp("mov", self.left, dest))
				code.append(ib.TwoOp("mov", self.right, reg))
				code.append(ib.TwoOp(self.opInstr(), reg, dest))
		
		r.free(reg)
		return code
	
	def flatten(self, inplace = False):
		leftPreStmts, self.left = self.left.flatten()
		rightPreStmts, self.right = self.right.flatten()
		
		preStmts = util.flatten([leftPreStmts, rightPreStmts])
		
		if inplace:
			return preStmts, self
		else:
			var = v.getVar()
			preStmts.append(Assign(var, self))
			return preStmts, var
	
	def getChildren(self):
		return [self.left, self.right]
	
	def opInstr(self):
		pass
	
	def opString(self):
		pass
	
	def toGraph(self):
		pass
	
	def toPython(self):
		return "{0} {1} {2}".format(self.left.toPython(), self.opString(), self.right.toPython())

class UnaryOp(Expression):
	def __init__(self, operand):
		self.operand = operand
	
	def compile(self, dest = None):
		code = ib.Block()

		if dest == None:
			code.append(ib.OneOp(self.opInstr(), self.operand.compile()))
		else:
			if isinstance(dest, Name):
				reg = r.alloc()
				
				code.append(ib.TwoOp("mov", self.operand.compile(), reg))
				code.append(ib.OneOp(self.opInstr(), reg))
				code.append(ib.TwoOp("mov", reg, dest))
				
				r.free(reg)
			else:
				code.append(ib.TwoOp("mov", self.operand.compile(), dest))
				code.append(ib.OneOp(self.opInstr(), dest))
		
		return code
	
	def flatten(self, inplace = False):
		preStmts, self.operand = self.operand.flatten()
		
		if inplace:
			return util.flatten(preStmts), self
		else:
			var = v.getVar()
			preStmts.append(Assign(var, self))
			return util.flatten(preStmts), var
	
	def getChildren(self):
		return [self.operand]
	
	def opInstr(self):
		pass
	
	def opString(self):
		pass
	
	def toGraph(self):
		pass
	
	def toPython(self):
		return "{0}{1}".format(self.opString(), self.operand.toPython())

class Negate(UnaryOp):
	def __repr__(self):
		return "Negate({0})".format(repr(self.operand))
	
	def opInstr(self):
		return "neg"
	
	def opString(self):
		return "-"

class Add(BinOp):
	def __repr__(self):
		return "Add(({0}, {1}))".format(repr(self.left), repr(self.right))
	
	def opInstr(self):
		return "add"
	
	def opString(self):
		return "+"

class Div(BinOp):
	def __repr__(self):
		return "Div(({0}, {1}))".format(repr(self.left), repr(self.right))
	
	def compile(self, dest = None):
		code = ib.Block()

		reg0 = r.alloc("%eax")
		reg1 = r.alloc("%ebx")
		reg2 = r.alloc("%edx")
		
		if isinstance(dest, Name):
			code.append(ib.TwoOp("mov", self.left, reg0))
			code.append(ib.TwoOp("mov", self.right, reg1))
			code.append(ib.Instruction("cltd"))
			
			code.append(ib.OneOp(self.opInstr(), reg1))
			code.append(ib.TwoOp("mov", reg0, dest))
		else:
			#This is broken for now.  Fixing it doesn't make sense until
			#register allocation is working.
			code.append(ib.TwoOp("mov", self.left, dest))
			code.append(ib.TwoOp("mov", self.right, reg0))
			code.append(ib.OneOp(self.opInstr(), dest))
		
		r.free(reg0)
		r.free(reg1)
		r.free(reg2)
		
		return code
	
	def opInstr(self):
		return "idiv"
	
	def opString(self):
		return "/"

class Mul(BinOp):
	def __repr__(self):
		return "Mul(({0}, {1}))".format(repr(self.left), repr(self.right))
	
	def opInstr(self):
		return "imul"
	
	def opString(self):
		return "*"

class Sub(BinOp):
	def __repr__(self):
		return "Sub(({0}, {1}))".format(repr(self.left), repr(self.right))
	
	def opInstr(self):
		return "sub"
	
	def opString(self):
		return "-"
