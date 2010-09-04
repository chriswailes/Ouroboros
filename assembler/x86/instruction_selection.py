"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/09/02
Description:	The instruction selection code for the x86 architecture.
"""

from assembler.x86 import memloc

from assembler import ib

import registers

from lib import ast

r = registers.RegisterFile()
s = memloc.Stack()

def selectInstructions(node, dest = None):
	global r
	global s
	
	if isinstance(node, ast.Assign):
		dest = selectInstructions(node.var)
		
		if isinstance(node.exp, ast.Name):
			code = ib.Block()
			reg = r.alloc()
			
			src = selectInstructions(node.exp)
			
			code.append(ib.TwoOp("mov", src, reg))
			code.append(ib.TwoOp("mov", reg, dest))
			r.free(reg)
			
			return code
		elif isinstance(node.exp, ast.Integer):
			src = selectInstructions(node.exp)
			
			return ib.TwoOp("mov", src, dest)
		else:
			return selectInstructions(node.exp, dest)
	
	elif isinstance(node, ast.BinOp) and not isinstance(node, ast.Div):
		code = ib.Block()
		reg = r.alloc()
		
		left = selectInstructions(node.left)
		right = selectInstructions(node.right)
		
		if isinstance(dest, memloc.Mem):
			code.append(ib.TwoOp("mov", left, reg))
			code.append(ib.TwoOp(node.opInstr(), right, reg))
			code.append(ib.TwoOp("mov", reg, dest))
		else:
			#In this case the destination is a register.
			code.append(ib.TwoOp("mov", left, dest))
			code.append(ib.TwoOp("mov", right, reg))
			code.append(ib.TwoOp(node.opInstr(), reg, dest))
		
		r.free(reg)
		return code
	
	elif isinstance(node, ast.Div):
		code = ib.Block()

		reg0 = r.alloc("%eax")
		reg1 = r.alloc("%ebx")
		reg2 = r.alloc("%edx")
		
		if isinstance(dest, memloc.Mem):
			code.append(ib.TwoOp("mov", node.left, reg0))
			code.append(ib.TwoOp("mov", node.right, reg1))
			code.append(ib.Instruction("cltd"))
			
			code.append(ib.OneOp(node.opInstr(), reg1))
			code.append(ib.TwoOp("mov", reg0, dest))
		else:
			#This is broken for now.  Fixing it doesn't make sense until
			#register allocation is working.
			code.append(ib.TwoOp("mov", node.left, dest))
			code.append(ib.TwoOp("mov", node.right, reg0))
			code.append(ib.OneOp(node.opInstr(), dest))
		
		r.free(reg0)
		r.free(reg1)
		r.free(reg2)
		
		return code
	
	elif isinstance(node, ast.FunctionCall):
		code = ib.Block()
		
		for arg in node.args:
			src = selectInstructions(arg)
			code.append(ib.OneOp("push", src))
		
		code.append(ib.OneOp("call", node.name.name, None))
		
		if len(node.args) > 0:
			size = str(len(node.args) * 4)
			code.append(ib.TwoOp("add", '$' + size, "%esp"))
		
		if dest:
			code.append(ib.TwoOp("mov", "%eax", dest))

		return code
	
	elif isinstance(node, ast.Integer):
		return "${0:d}".format(node.value)
	
	elif isinstance(node, ast.Module):
		stack = memloc.Stack()
		subCode = ib.Block()
		
		code = ib.Block()
		code.header  = "# x86\n"
		code.header += ".globl main\n"
		code.header += "main:\n"
		
		#Push the old base pointer onto the stack.
		code.append(ib.OneOp("push", "%ebp"))
		#Make the old stack pointer the new base pointer.
		code.append(ib.TwoOp("mov", "%esp", "%ebp"))
		
		for stmt in node.stmts:
			subCode.append(selectInstructions(stmt))
		
		#Expand the stack.
		code.append(ib.TwoOp("sub", "$" + str(s.size), "%esp"))
		
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
	
	elif isinstance(node, ast.Name):
		return s.getAddr(node.name)
	
	elif isinstance(node, ast.UnaryOp):
		code = ib.Block()
		
		src = selectInstructions(node.operand)
		
		if dest == None:
			code.append(ib.OneOp(node.opInstr(), src))
		else:
			if isinstance(dest, memloc.Mem):
				reg = r.alloc()
				
				code.append(ib.TwoOp("mov", src, reg))
				code.append(ib.OneOp(node.opInstr(), reg))
				code.append(ib.TwoOp("mov", reg, dest))
				
				r.free(reg)
			else:
				code.append(ib.TwoOp("mov", src, dest))
				code.append(ib.OneOp(node.opInstr(), dest))
		
		return code
	
