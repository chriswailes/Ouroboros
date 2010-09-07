"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/09/02
Description:	The instruction selection code for the x86 architecture.
"""

from assembler.x86.memloc import *
from assembler.x86.registers import *
from assembler.x86.ib import *

from lib import ast

r = RegisterFile()
s = Stack()

def selectInstructions(node, dest = None):
	global r
	global s
	
	#Make sure we aren't accidentally passing in some odd value for the desired
	#destination.
	if not (dest == None or isinstance(dest, Mem) or isinstance(dest, Register)):
		raise Exception('Invalid destination.')
	
	if isinstance(node, ast.Assign):
		#The destination is going to be a name, so we need to translate it
		#into a Mem object.
		dest = selectInstructions(node.var)
		
		if isinstance(node.exp, ast.Name):
			code = Block()
			reg = r.alloc()
			
			#Here we know the node.exp is a name.  Thus, we need to translate
			#it into a Mem object.
			src = selectInstructions(node.exp)
			
			code.append(TwoOp("mov", src, reg))
			code.append(TwoOp("mov", reg, dest))
			r.free(reg)
			
			return code
		elif isinstance(node.exp, ast.Integer):
			src = selectInstructions(node.exp)
			
			return TwoOp("mov", src, dest)
		else:
			#Here the right side of the assignment is a complex expression.
			#We will select instructions for it, giving the Mem object
			#representing the variable's location as the destination.
			return selectInstructions(node.exp, dest)
	
	elif isinstance(node, ast.BinOp):
		code = Block()
		reg = r.alloc()
		
		#The left and right operands need to be translated, but the
		#destination is already a Mem object or a register.
		left = selectInstructions(node.left)
		right = selectInstructions(node.right)
		
		if isinstance(node, ast.Add):
			if isinstance(left, Immediate) and left.value == 1:
				if isinstance(dest, Mem):
					code.append(TwoOp('mov', right, reg))
					code.append(OneOp('inc', reg))
					code.append(TwoOp('mov', reg, dest))
				else:
					code.append(TwoOp('mov', right, dest))
					code.append(OneOp('inc', dest))
			
			elif isinstance(right, Immediate) and right.value == 1:
				if isinstance(dest, Mem):
					code.append(TwoOp('mov', left, reg))
					code.append(OneOp('inc', reg))
					code.append(TwoOp('mov', reg, dest))
				else:
					code.append(TwoOp('mov', left, dest))
					code.append(OneOp('inc', dest))
			
			else:
				if isinstance(dest, Mem):
					code.append(TwoOp('mov', left, reg))
					code.append(TwoOp('add', right, reg))
					code.append(TwoOp('mov', reg, dest))
				else:
					#In this case the destination is a register.  If it
					#isn't, the error will be caught by the ib module.
					code.append(TwoOp('mov', left, dest))
					code.append(TwoOp('mov', right, reg))
					code.append(TwoOp('add', reg, dest))
			
		elif isinstance(node, ast.Div):
			if isinstance(right, Immediate) and (right.value % 2) == 0 and (right.value / 2) < 31:
				#We can shift to the right instead of dividing.
				dist = right.value / 2
				
				if isinstance(dest, Mem):
					code.append(TwoOp('mov', left, reg))
					code.append(TwoOp('sar', Immediate(dist), reg))
					code.append(TwoOp('mov', reg, dest))
				else:
					code.append(TwoOp('mov', left, dest))
					code.append(TwoOp('sar', Immediate(dist), dest))
			else:
				#This is broken for now.  Fixing it doesn't make sense until
				#register allocation is working.
				
				reg0 = r.alloc("eax")
				reg1 = r.alloc("ebx")
				reg2 = r.alloc("edx")
				
				if isinstance(dest, Mem):
					code.append(TwoOp("mov", left, reg0))
					code.append(TwoOp("mov", right, reg1))
					code.append(Instruction("cltd"))
					
					code.append(OneOp(node.opInstr(), reg1))
					code.append(TwoOp("mov", reg0, dest))
				else:
					code.append(TwoOp("mov", node.left, dest))
					code.append(TwoOp("mov", node.right, reg0))
					code.append(OneOp(node.opInstr(), dest))
				
				r.free(reg0)
				r.free(reg1)
				r.free(reg2)
		
		elif isinstance(node, ast.Mul):
			if isinstance(left, Immediate) and (left.value % 2) == 0 and (left.value / 2) < 31:
				#We can shift to the left instead of multiplying.
				dist = left.value / 2
				
				if isinstance(dest, Mem):
					code.append(TwoOp('mov', right, reg))
					code.append(TwoOp('sal', Immediate(dist), reg))
					code.append(TwoOp('mov', reg, dest))
				else:
					code.append(TwoOp('mov', right, dest))
					code.append(TwoOp('sal', Immediate(dist), dest))
			
			elif isinstance(right, Immediate) and (right.value % 2) == 0 and (right.value / 2) < 31:
				#We can shift to the left instead of multiplying.
				dist = right.value / 2
				
				if isinstance(dest, Mem):
					code.append(TwoOp('mov', left, reg))
					code.append(TwoOp('sal', Immediate(dist), reg))
					code.append(TwoOp('mov', reg, dest))
				else:
					code.append(TwoOp('mov', left, dest))
					code.append(TwoOp('sal', Immediate(dist), dest))
			
			else:
				if isinstance(dest, Mem):
					code.append(TwoOp('mov', left, reg))
					code.append(TwoOp('imul', right, reg))
					code.append(TwoOp('mov', reg, dest))
				else:
					code.append(TwoOp('mov', left, dest))
					code.append(TwoOp('mov', right, reg))
					code.append(TwoOp('imul', reg, dest))
		
		elif isinstance(node, ast.Sub):
			if isinstance(right, Immediate) and right.value == 1:
				if isinstance(dest, Mem):
					code.append(TwoOp('mov', left, reg))
					code.append(OneOp('dec', reg))
					code.append(TwoOp('mov', reg, dest))
				else:
					code.append(TwoOp('mov', left, dest))
					code.append(OneOp('dec', dest))
			else:
				if isinstance(dest, Mem):
					code.append(TwoOp('mov', left, reg))
					code.append(TwoOp('sub', right, reg))
					code.append(TwoOp('mov', reg, dest))
				else:
					code.append(TwoOp('mov', left, dest))
					code.append(TwoOp('mov', right, reg))
					code.append(TwoOp('sub', reg, dest))
		
		r.free(reg)
		return code
	
	elif isinstance(node, ast.FunctionCall):
		code = Block()
		
		for arg in node.args:
			src = selectInstructions(arg)
			code.append(OneOp("push", src))
		
		code.append(OneOp("call", node.name.name, None))
		
		if len(node.args) > 0:
			size = str(len(node.args) * 4)
			code.append(TwoOp("add", Immediate(size), Register("esp")))
		
		if dest:
			code.append(TwoOp("mov", Register("eax"), dest))

		return code
	
	elif isinstance(node, ast.Integer):
		return Immediate(node.value)
	
	elif isinstance(node, ast.Module):
		stack = Stack()
		subCode = Block()
		
		code = Block()
		code.header  = "# x86\n"
		code.header += ".globl main\n"
		code.header += "main:\n"
		
		#Push the old base pointer onto the stack.
		code.append(OneOp("push", Register("ebp")))
		#Make the old stack pointer the new base pointer.
		code.append(TwoOp("mov", Register("esp"), Register("ebp")))
		
		for stmt in node.stmts:
			subCode.append(selectInstructions(stmt))
		
		#Expand the stack.
		code.append(TwoOp("sub", Immediate(s.size), Register("esp")))
		
		code.append(subCode)
		
		endBlock = Block()
		#Put our exit value in %eax
		endBlock.append(TwoOp("mov", Immediate(0), Register("eax")))
		#Restore the stack.
		endBlock.append(Instruction("leave"))
		#Return
		endBlock.append(Instruction("ret"))

		code.append(endBlock)
		
		return code
	
	elif isinstance(node, ast.Name):
		return s.getAddr(node.name)
	
	elif isinstance(node, ast.UnaryOp):
		code = Block()
		
		src = selectInstructions(node.operand)
		
		if dest == None:
			code.append(OneOp(node.opInstr(), src))
		else:
			if isinstance(dest, Mem):
				reg = r.alloc()
				
				code.append(TwoOp("mov", src, reg))
				code.append(OneOp(node.opInstr(), reg))
				code.append(TwoOp("mov", reg, dest))
				
				r.free(reg)
			elif isinstance(dest, Register):
				code.append(TwoOp("mov", src, dest))
				code.append(OneOp(node.opInstr(), dest))
			else:
				raise Exception("Invalid destination.")
		
		return code
	
