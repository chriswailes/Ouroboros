"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/09/02
Description:	The instruction selection code for the x86 architecture.
"""

from assembler import *
from assembler.coloring import *
from assembler.x86.ib import *
from assembler.x86.coloring import eax, ebp, esp, callee, caller

from lib import ast

l = Labeler()

def selectInstructions(node, cf, dest = None):
	global l
	
	if isinstance(node, ast.Assign):
		#The destination is a name, so we need to translate it.
		dest = selectInstructions(node.var, cf)
		
		if isinstance(node.exp, ast.Name):
			code = Block()
			
			#The source is a name, so we need to translate it.
			src = selectInstructions(node.exp, cf)
			
			if isinstance(src, Mem) and isinstance(dest, Mem):
				
				tmpColor = getTempColor(cf, node)
				
				code.append(TwoOp('mov', src, tmpColor))
				code.append(TwoOp('mov', tmpColor, dest))
			
			elif src != dest:
				code.append(TwoOp('mov', src, dest))
			
			return code
		elif isinstance(node.exp, ast.Integer):
			src = selectInstructions(node.exp, cf)
			src = pack(src, Integer)
			
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
		savedLeft = left = selectInstructions(node.left, cf)
		savedRight = right = selectInstructions(node.right, cf)
		
		#########
		# Setup #
		#########
		
		#This code will make sure that both the right and left parameters are
		#in registers.
		
		tmpColor0 = getTempColor(cf, node) if isinstance(dest, Mem) else dest
			
		if isinstance(left, Mem):
			if right != dest:
				code.append(TwoOp('mov', left, tmpColor0))
				left = tmpColor0
			
			else:
				tmpcolor1 = getTempColor(cf, node) if tmpColor0 == dest else tmpColor0
				code.append(TwoOp('mov', left, tmpColor1))
				left = tmpColor1
		
		elif isinstance(left, Immediate) and (isinstance(node, Div) or isinstance(node, Sub)):
			#Move left hand immediates into the temporary register when it is
			#a divide or subtract operation.
			code.append(TwoOp('mov', left, tmpColor0))
			left = tmpColor0
		
		if isinstance(right, Mem):
			if left != tmpColor0 and (isinstance(node, Add) or isinstance(node, Mul)):
				code.append(TwoOp('mov', right, tmpColor0))
				left = right
				right = tmpColor0
			
			else:
				tmpColor1 = getTempColor(cf, node, tmpColor0)
				
				code.append(TwoOp('mov', right, tmpColor1))
				right = tmpColor1
		
		#Untag the left operand if it isn't an immediate.
		if isinstance(savedLeft, Color):
			code.append(untag(left))
		
		#Untag the right operand if it isn't an immediate.
		if isinstance(savedRight, Color) and savedLeft != savedRight:
			code.append(untag(right))
		
		#############
		# End Setup #
		#############
		
		#The right value is never going to be an immediate due to our constant
		#folding transformation.
		
		if isinstance(node, ast.Add):
			if isinstance(left, Immediate) and left.value == 1:
				code.append(OneOp('inc', right))
			
			elif right == dest or isinstance(left, Immediate):
				code.append(TwoOp('add', left, right))
			
			else:
				code.append(TwoOp('add', right, left))
			
		elif isinstance(node, ast.Div):
			if isinstance(right, Immediate) and (right.value % 2) == 0 and (right.value / 2) < 31:
				#We can shift to the right instead of dividing.
				dist = right.value / 2
				
				#FIXME
			else:
				#FIXME
				pass
		
		elif isinstance(node, ast.Mul):
			if isinstance(left, Immediate) and (left.value % 2) == 0 and (left.value / 2) < 31:
				#We can shift to the left instead of multiplying.
				dist = left.value / 2
				
				code.append(TwoOp('sal', Immediate(dist), right))
			
			elif right == dest or isinstance(left, Immediate):
				code.append(TwoOp('imul', left, right))
			
			else:
				code.append(TwoOp('imul', right, left))
		
		elif isinstance(node, ast.Sub):
			if isinstance(right, Immediate) and right == 1:
				code.append(OneOp('dec', left))
			
			else:
				code.append(TwoOp('sub', right, left))
		
		###########
		# Cleanup #
		###########
		
		#Re-tag left, right, and result appropriately.
		code.append(tag(tmpColor0, Integer))
		
		if savedLeft != dest and isinstance(savedLeft, Register) and savedLeft in toColors(node['post-alive']) :
			code.append(tag(savedLeft, Integer))
		
		if savedRight != dest and isinstance(savedRight, Register) and savedRight in toColors(node['post-alive']):
			code.append(tag(savedRight, Integer))
		
		#Move the result.
		if tmpColor0 != dest:
			code.append(TwoOp('mov', tmpColor0, dest))
		
		###############
		# End Cleanup #
		###############
		
		return code
	
	elif isinstance(node, ast.FunctionCall):
		code = Block()
		
		usedColors = toColors(node['pre-alive'])
		
		#Save any caller saved registers currently in use.
		saveRegs(code, caller, usedColors)
		
		first = True
		addSize = 0
		for arg in node.args:
			src = selectInstructions(arg, cf)
			if isinstance(src, Immediate):
				src = pack(src, Integer)
			
			if first and len(code.insts) > 0:
				inst = code.insts[-1]
				
				if not (isinstance(inst, OneOp) and inst.name == 'push' and inst.operand == src):
					code.append(OneOp('push', src))
					addSize += 4
			
			else:
				code.append(OneOp('push', src))
				addSize += 4
			
			first = False
		
		#Make the function call.
		code.append(OneOp('call', node.name.symbol, None))
		
		#Restore the stack.
		if addSize > 0:
			code.append(TwoOp('add', Immediate(addSize), esp))
		
		#Move the result into the proper destination.
		if dest and dest != eax:
			code.append(TwoOp('mov', eax, dest))
		
		#Restore any caller saved registers that are in use.
		restoreRegs(code, caller, usedColors)

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
		code.append(OneOp('push', ebp))
		#Make the old stack pointer the new base pointer.
		code.append(TwoOp('mov', esp, ebp))
		
		usedColors = toColors(node.collectSymbols())
		
		#Save any callee saved registers we used.
		saveRegs(code, callee, usedColors)
		
		#Expand the stack.
		if cf.offset > 0:
			code.append(TwoOp('sub', Immediate(cf.offset), esp))
		
		#Append the module's code.
		code.append(selectInstructions(node.block, cf))
		
		endBlock = Block()
		#Restore the stack.
		if cf.offset > 0:
			endBlock.append(TwoOp('add', Immediate(cf.offset), esp))
		
		#Restore any callee saved registers we used.
		restoreRegs(endBlock, callee, usedColors)
		
		#Put our exit value in %eax
		endBlock.append(TwoOp('mov', Immediate(0), eax))
		#Restore the %esp and %ebp registers.
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
	
	elif isinstance(node, ast.Negate):
		code = Block()
		
		src = selectInstructions(node.operand, cf)
		
		#########
		# Setup #
		#########
		
		tmpColor = getTempColor(cf, node) if isinstance(dest, Mem) else dest
		
		if src != tmpColor:
			code.append(TwoOp('mov', src, tmpColor))
		
		code.append(untag(tmpColor))
		
		#############
		# End Setup #
		#############
		
		code.append(OneOp('neg', dest))
		
		###########
		# Cleanup #
		###########
		
		code.append(tag(tmpColor, Integer))
		
		if tmpColor != dest:
			code.append(TwoOp('mov', tmpColor, dest))
		
		###############
		# End Cleanup #
		###############
		
		return code
