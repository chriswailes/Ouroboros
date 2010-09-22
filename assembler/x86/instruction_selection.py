"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/09/02
Description:	The instruction selection code for the x86 architecture.
"""

from assembler.coloring import *
from assembler.x86.ib import *

from lib import ast

l = Labeler()

def selectInstructions(node, cf, dest = None):
	global l
	
	if not isinstance(node, ast.Name):
		tmpColor = cf.getColor(node['pre-alive'], test = Register)
	
	if isinstance(node, ast.Assign):
		#The destination is a name, so we need to translate it.
		dest = selectInstructions(node.var, cf)
		
		if isinstance(node.exp, ast.Name):
			code = Block()
			
			#The source is a name, so we need to translate it.
			src = selectInstructions(node.exp, cf)
			
			if isinstance(src, Mem) and isinstance(dest, Mem):
				code.append(TwoOp('mov', src, tmpColor))
				code.append(TwoOp('mov', tmpColor, dest))
			
			else:
				code.append(TwoOp('mov', src, dest))
			
			return code
		elif isinstance(node.exp, ast.Integer):
			src = selectInstructions(node.exp, cf)
			
			return TwoOp('mov', src, dest)
		else:
			#Here the right side of the assignment is a complex expression.
			#We will select instructions for it, giving the Symbol
			#representing the variable's location as the destination.
			return selectInstructions(node.exp, cf, dest)
	
	elif isinstance(node, ast.BasicBlock):
		code = Block()
		
		for child in node:
			code.append(selectInstructions(child, cf))
		
		return code
	
	elif isinstance(node, ast.BinOp):
		code = Block()
		
		#The left and right operands need to be translated, but the
		#destination is already a Symbol,
		left = selectInstructions(node.left, cf)
		right = selectInstructions(node.right, cf)
		
		if isinstance(node, ast.Add):
			#The right value is never going to be an immediate due to our
			#constant folding transformation.
			
			if isinstance(left, Immediate) and left.value == 1:
				if isinstance(dest, Mem):
					code.append(TwoOp('mov', right, tmpColor))
					code.append(OneOp('inc', tmpColor))
					code.append(TwoOp('mov', tmpColor, dest))
				
				else:
					code.append(TwoOp('mov', right, dest))
					code.append(OneOp('inc', dest))
			
			else:
				if isinstance(dest, Mem):
					code.append(TwoOp('mov', left, tmpColor))
					code.append(TwoOp('add', right, tmpColor))
					code.append(TwoOp('mov', tmpColor, dest))
				
				else:
					code.append(TwoOp('mov', left, dest))
					code.append(TwoOp('add', right, dest))
			
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
		
		elif isinstance(node, ast.Mul):
			if isinstance(left, Immediate) and (left.value % 2) == 0 and (left.value / 2) < 31:
				#We can shift to the left instead of multiplying.
				dist = left.value / 2
				
				if isinstance(dest, Mem):
					code.append(TwoOp('mov', right, tmpColor))
					code.append(TwoOp('sal', Immediate(dist), tmpColor))
					code.append(TwoOp('mov', tmpColor, dest))
				
				else:
					code.append(TwoOp('mov', right, dest))
					code.append(TwoOp('sal', Immediate(dist), dest))
			
			elif isinstance(right, Immediate) and (right.value % 2) == 0 and (right.value / 2) < 31:
				#We can shift to the left instead of multiplying.
				dist = right.value / 2
				
				if isinstance(dest, Mem):
					code.append(TwoOp('mov', left, tmpColor))
					code.append(TwoOp('sal', Immediate(dist), tmpColor))
					code.append(TwoOp('mov', tmpColor, dest))
				
				else:
					code.append(TwoOp('mov', left, dest))
					code.append(TwoOp('sal', Immediate(dist), dest))
			
			else:
				if isinstance(dest, Mem):
					code.append(TwoOp('mov', left, tmpColor))
					code.append(TwoOp('imul', right, tmpColor))
					code.append(TwoOp('mov', tmpColor, dest))
				
				else:
					code.append(TwoOp('mov', left, dest))
					code.append(TwoOp('imul', right, dest))
		
		elif isinstance(node, ast.Sub):
			if isinstance(right, Immediate) and right.value == 1:
				if isinstance(dest, Mem):
					code.append(TwoOp('mov', left, tmpColor))
					code.append(OneOp('dec', tmpColor))
					code.append(TwoOp('mov', tmpColor, dest))
				
				else:
					code.append(TwoOp('mov', left, dest))
					code.append(OneOp('dec', dest))
			
			else:
				if isinstance(dest, Mem):
					code.append(TwoOp('mov', left, tmpColor))
					code.append(TwoOp('sub', right, tmpColor))
					code.append(TwoOp('mov', tmpColor, dest))
				
				else:
					code.append(TwoOp('mov', left, dest))
					code.append(TwoOp('sub', right, dest))
		
		return code
	
	elif isinstance(node, ast.FunctionCall):
		code = Block()
		
		for arg in node.args:
			src = selectInstructions(arg, cf)
			code.append(OneOp('push', src))
		
		code.append(OneOp('call', node.name.symbol, None))
		
		if len(node.args) > 0:
			size = str(len(node.args) * 4)
			code.append(TwoOp('add', Immediate(size), Register('esp')))
		
		if dest:
			code.append(TwoOp('mov', Register('eax'), dest))

		return code
	
	elif isinstance(node, ast.If):
		if isinstance(node.cond, ast.Integer):
			if node.cond.value != 0:
				return selectInstructions(node.then, cf)
			else:
				return selectInstructions(node.els, cf)
		
		else:
			#In this case the condition is a variable.
			code = Block()
			elsLabel = l.nextLabel()
			endLabel = l.nextLabel()
			
			cond = selectInstructions(node.cond, cf)
			
			code.append(TwoOp('cmp', Immediate(0), cond))
			code.append(OneOp('jz', elsLabel, None))
			
			#Now the then case
			code.append(selectInstructions(node.then, cf))
			code.append(OneOp('jmp', endLabel, None))
			
			#Now the label and the else case.
			code.append(elsLabel)
			code.append(selectInstructions(node.els, cf))
			code.append(endLabel)
			
			return code
	
	elif isinstance(node, ast.Integer):
		return Immediate(node.value)
	
	elif isinstance(node, ast.Module):
		code = Block()
		code.header  = "# x86\n"
		code.header += ".globl main\n"
		code.header += "main:\n"
		
		#Push the old base pointer onto the stack.
		code.append(OneOp('push', Register('ebp')))
		#Make the old stack pointer the new base pointer.
		code.append(TwoOp('mov', Register('esp'), Register('ebp')))
		
		#Expand the stack.
		if cf.offset > 0:
			code.append(TwoOp('sub', cf.offset, Register('esp')))
		
		#Append the module's code.
		code.append(selectInstructions(node.block, cf))
		
		endBlock = Block()
		#Put our exit value in %eax
		endBlock.append(TwoOp('mov', Immediate(0), Register('eax')))
		#Restore the stack.
		endBlock.append(Instruction('leave'))
		#Return
		endBlock.append(Instruction('ret'))

		code.append(endBlock)
		
		return code
	
	elif isinstance(node, ast.Name):
		if node.symbol.has_key('color'):
			return node.symbol['color']
		else:
			return node.symbol
	
	elif isinstance(node, ast.UnaryOp):
		code = Block()
		
		src = selectInstructions(node.operand, cf)
		
		if dest == None:
			code.append(OneOp(node.opInstr(), src))
		
		else:
			if isinstance(dest, Mem):
				code.append(TwoOp("mov", src, tmpColor))
				code.append(OneOp(node.opInstr(), tmpColor))
				code.append(TwoOp("mov", tmpColor, dest))
				
			else:
				code.append(TwoOp("mov", src, dest))
				code.append(OneOp(node.opInstr(), dest))
		
		return code
	
