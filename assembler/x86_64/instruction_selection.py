"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/09/02
Description:	The instruction selection code for the x86 architecture.
"""

from assembler.x86_64 import ib, registers

from lib import ast
from lib import variables as v

def selectInstructions(node, dest = None):
	r = registers.RegisterFile()
	
	if isinstance(node, ast.Assign):
		if isinstance(node.exp, ast.Name):
			code = ib.Block()
			
			reg = r.alloc()
			code.append(ib.TwoOp("mov", selectInstructions(node.exp), reg))
			code.append(ib.TwoOp("mov", reg, node.var))
			r.free(reg)
			
			return code
		elif isinstance(node.exp, ast.Integer):
			return ib.TwoOp("mov", selectInstructions(node.exp), node.var)
		else:
			return selectInstructions(node.exp, node.var)
	
	elif isinstance(node, ast.BinOp) and not isinstance(node, ast.Div):
		code = ib.Block()
		reg = r.alloc()
		
		if isinstance(dest, ast.Name):
			code.append(ib.TwoOp("mov", node.left, reg))
			code.append(ib.TwoOp(node.opInstr(), node.right, reg))
			code.append(ib.TwoOp("mov", reg, dest))
		else:
			#In this case the destination is a register.
			code.append(ib.TwoOp("mov", node.left, dest))
			code.append(ib.TwoOp("mov", node.right, reg))
			code.append(ib.TwoOp(node.opInstr(), reg, dest))
		
		r.free(reg)
		return code
	
	elif isinstance(node, ast.Div):
		code = ib.Block()

		reg0 = r.alloc("%rax")
		reg1 = r.alloc("%rbx")
		reg2 = r.alloc("%rdx")
		
		if isinstance(dest, ast.Name):
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
			reg = r.nextArgReg()
			src = selectInstructions(arg)
			
			if reg:
				code.append(ib.TwoOp("mov", src, reg))
			else:
				code.append(ib.OneOp("push", src))
		
		code.append(ib.OneOp("call", node.name.name, None))
		
		if len(node.args) > 4:
			size = str((len(node.args) - 4) * 4)
			code.append(ib.TwoOp("add", '$' + size, "%rsp"))
		
		if dest:
			code.append(ib.TwoOp("mov", "%rax", selectInstructions(dest)))

		return code
	
	elif isinstance(node, ast.Integer):
		return "${0:d}".format(node.value)
	
	elif isinstance(node, ast.Module):
		code = ib.Block()
		code.header  = "# x86_64\n"
		code.header += ".globl main\n"
		code.header += "main:"
		
		for stmt in node.stmts:
			code.append(selectInstructions(stmt))
		
		endBlock = ib.Block()
		#Put our exit value in %rax
		endBlock.append(ib.TwoOp("mov", "$0", "%rax"))
		#Return
		endBlock.append(ib.Instruction("ret"))

		code.append(endBlock)
		
		return code
	
	elif isinstance(node, ast.Name):
		return "{0:d}(%rsp)".format(v.getVarLoc(node.name))
	
	elif isinstance(node, ast.UnaryOp):
		code = ib.Block()

		if dest == None:
			code.append(ib.OneOp(node.opInstr(), selectInstructions(node.operand)))
		else:
			if isinstance(dest, ast.Name):
				reg = r.alloc()
				
				code.append(ib.TwoOp("mov", selectInstructions(node.operand), reg))
				code.append(ib.OneOp(node.opInstr(), reg))
				code.append(ib.TwoOp("mov", reg, dest))
				
				r.free(reg)
			else:
				code.append(ib.TwoOp("mov", selectInstructions(node.operand), dest))
				code.append(ib.OneOp(node.opInstr(), dest))
		
		return code
	
