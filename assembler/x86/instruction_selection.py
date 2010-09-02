"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/09/02
Description:	The instruction selection code for the x86 architecture.
"""

from assembler import ib

from lib import ast
from lib import registers as r
from lib import variables as v

def selectInstructions(node, dest = None):
	if isinstance(node, ast.Assign):
		if isinstance(node.exp, ast.Name):
			code = ib.Block()
			
			reg = r.alloc()
			code.append(ib.TwoOp("mov", selectInstructions(node.exp), reg))
			code.append(ib.TwoOp("mov", reg, self.var))
			
			r.free(reg)
			
			return code
		else:
			return selectInstructions(node.exp, node.var)
	
	elif isinstance(node, ast.BinOp) and not isinstance(node, ast.Div):
		code = ib.Block()
		reg = r.alloc()

		if isinstance(node.left, ast.Integer) and isinstance(node.right, ast.Integer):
			value = ast.Integer(eval("{0:d} {1} {2:d}".format(node.left.value, node.opString(), node.right.value)))
			code.append(ib.TwoOp("mov", value, dest))

		else:
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

		reg0 = r.alloc("%eax")
		reg1 = r.alloc("%ebx")
		reg2 = r.alloc("%edx")
		
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
			code.append(ib.OneOp("push", selectInstructions(arg)))
		
		code.append(ib.OneOp("call", node.name.name, None))
		
		if len(node.args) > 0:
			size = str(len(node.args) * 4)
			code.append(ib.TwoOp("add", '$' + size, "%esp"))
		
		if dest:
			code.append(ib.TwoOp("mov", "%eax", dest))

		return code
		
		code.append(ib.OneOp("push", selectInstructions(node.args[0])))
		code.append(ib.OneOp("call", "print_int_nl", None))
		code.append(ib.TwoOp("add", "$4", "%esp"))
	
	elif isinstance(node, ast.Integer):
		return "${0:d}".format(node.value)
	
	elif isinstance(node, ast.Module):
		subCode = ib.Block()
		
		code = ib.Block()
		code.header  = ".globl main\n"
		code.header += "main:\n"
		
		#Push the old base pointer onto the stack.
		code.append(ib.OneOp("push", "%ebp"))
		#Make the old stack pointer the new base pointer.
		code.append(ib.TwoOp("mov", "%esp", "%ebp"))
		
		for stmt in node.stmts:
			subCode.append(selectInstructions(stmt))
		
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
	
	elif isinstance(node, ast.Name):
		return "-{0:d}(%ebp)".format(v.getVarLoc(node.name))
	
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
	
