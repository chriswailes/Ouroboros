"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/09/02
Description:	The instruction selection code for the x86 architecture.
"""

from assembler.coloring import *
from assembler.tagging import *

from assembler.x86.ib import *
from assembler.x86.coloring import eax, ebp, esp, callee, caller

from lib import ast
from lib.util import classGuard

def selectInstructions(node, cf, dest = None):
	
	#Error out if we receive a complex node that should have been flattened
	#or translated out before instruction selection.
	if not node.isSimple():
		raise Exception('Non-simple node passed to instruction selection pass.')
	
	if isinstance(node, ast.Assign):
		#The destination is a name, so we need to translate it.
		dest = selectInstructions(node.var, cf)
		
		if isinstance(node.exp, ast.Symbol):
			code = Block('')
			
			#The source is a name, so we need to translate it.
			src = selectInstructions(node.exp, cf)
			
			if isinstance(src, Mem) and isinstance(dest, Mem):
				
				tmpColor = getTmpColor(cf, node)
				
				code.append(move(src, tmpColor))
				code.append(move(tmpColor, dest))
			
			elif src != dest:
				code.append(mvoe(src, dest))
			
			return code
		elif isinstance(node.exp, ast.Integer):
			src = selectInstructions(node.exp, cf)
			src = pack(src, INT)
			
			return move(src, dest)
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
		origLeft = left = selectInstructions(node.left, cf)
		origRight = right = selectInstructions(node.right, cf)
		
		#########
		# Setup #
		#########
		
		#This code will make sure that both the right and left parameters are
		#in registers.
		
		#tmpColor0 will be a register, and hold the final result of our
		#computation.  The result may need to be moved if tmpColor0 is not
		#the destination.
		tmpColor0 = getTmpColor(cf, node) if isinstance(dest, Mem) else dest
			
		if isinstance(left, Mem):
			if right != dest:
				code.append(move(left, tmpColor0))
				left = tmpColor0
			
			else:
				tmpColor1 = getTmpColor(cf, node) if tmpColor0 == dest else tmpColor0
				code.append(move(left, tmpColor1))
				left = tmpColor1
		
		elif isinstance(left, Immediate):
			if classGuard(node, ast.Div, ast.Sub):
				#Move left hand immediates into the temporary register when it is
				#a divide or subtract operation.
				
				tmpColor1 = getTmpColor(cf, node) if right == tmpColor0 else tmpColor0
				
				if right == tmpColor0:
					code.append(move(right, tmpColor1))
					right = tmpColor1
				
				code.append(move(left, tmpColor0))
				left = tmpColor0
					
			elif right != dest:
				#If the left hand value is an immediate and this is an add
				#or multiply operation the right hand value needs to be in
				#the destination register.
				code.append(move(right, tmpColor0))
				right = tmpColor0
		
		elif isinstance(left, Register) and left != dest:
			code.append(move(left, tmpColor0))
			left = tmpColor0
		
		if isinstance(right, Mem):
			if left != tmpColor0 and classGuard(node, Add, Mul) and not isinstance(node, Logical):
				code.append(move(right, tmpColor0))
				left = right
				right = tmpColor0
			
			else:
				tmpColor1 = getTmpColor(cf, node, tmpColor0)
				
				code.append(move(right, tmpColor1))
				right = tmpColor1
		
		#Untag the left operand if it isn't an immediate.
		if isinstance(left, Color) and classGuard(node, ast.Div, ast.Mul, ast.Sub) and left.tagged:
			code.append(untag(left))
		
		#Untag the right operand if it isn't an immediate.
		if right != left and isinstance(right, Color) and classGuard(node, ast.Div, ast.Mul, ast.Sub) and right.tagged:
			code.append(untag(right))
		
		#############
		# End Setup #
		#############
		
		if isinstance(node, ast.Add):
			#The right value is never going to be an immediate due to our
			#constant folding transformation.
			if isinstance(left, Immediate):
				
				#This value hasn't been untagged yet.
				code.append(untag(tmpColor0))
				
				if left.value == 1:
					code.append(OneOp('inc', tmpColor0))
				
				else:
					code.append(TwoOp('add', left, tmpColor0))
				
				#Cause the result to be tagged as an integer.
				tmpColor0.tag = INT
			
			else:
				#Build the case where we need to call the add function.
				case0 = Block()
				case0.append(OneOp('push', right))
				case0.append(OneOp('push', left))
				case0.append(OneOp('call', ast.Name('add'), None))
				case0.append(TwoOp('sub', Immediate(8), esp))
				case0.append(tag(eax, OBJ))
				
				if eax != dest:
					case0.append(move(eax, tmpColor0))
				
				#Build the case where we are adding two integers.
				case1 = Block()
				
				#Untag values as necessary.
				case1.append(untag(left))
				
				if left != right:
					case1.append(untag(right))
				
				#Decide which operand to add to which.
				if left == tmpColor0:
					case1.append(TwoOp('add', right, tmpColor0))
				
				else:
					case1.append(TwoOp('add', left, tmpColor0))
				
				#Tag the result of the integer addition.
				case1.append(tag(tmpColor0, INT))
				
				#Re-tag the operands.
				if left != tmpColor0:
					case1.append(tag(left, INT))
				
				if right != tmpColor0:
					case1.append(tag(right, INT))
				
				code.append(buildITE(tmpColor0, case0, case1, TAG_MASK, 'je', True))
			
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
				
				code.append(TwoOp('sal', Immediate(dist), tmpColor0))
			
			elif right == dest or isinstance(left, Immediate):
				code.append(TwoOp('imul', left, tmpColor0))
			
			else:
				code.append(TwoOp('imul', right, tmpColor0))
			
			tmpColor0.tag = INT
		
		elif isinstance(node, ast.Sub):
			if isinstance(right, Immediate) and right == 1:
				code.append(OneOp('dec', tmpColor0))
			
			else:
				code.append(TwoOp('sub', right, tmpColor0))
			
			tmpColor0.tag = INT
		
		elif isinstance(node, ast.And):
			if left == dest:
				case0 = move(right, tmpColor0)
				case1 = None
			
			else:
				case0 = move(right, tmpColor0)
				case1 = move(left, tmpColor0)
				
			code.append(buildITE(left, case0, case1, FALS, 'jl', True))
		
		elif isinstance(node, ast.Or):
			if left == dest:
				case0 = move(right, tmpColor0)
				case1 = None
			
			else:
				case0 = move(right, tmpColor0)
				case1 = move(left, tmpColor0)
				
			code.append(buildITE(left, case0, case1, FALS, 'jg', True))
		
		elif isinstance(node, ast.Eq):
			tagType = None
				
			case0 = Block()
			
			#Build the case where we need to call the equal function.
			case0.append(OneOp('push', right))
			case0.append(OneOp('push', left))
			case0.append(OneOp('call', ast.Name('equal'), None))
			case0.append(TwoOp('sub', Immediate(8), esp))
			case0.append(tag(eax, BOOL))
			case0.append(move(eax, tmpColor0))
			
			case2 = move(TRU, tmpColor0)
			case3 = move(FALS, tmpColor0)
			
			#Build the case where we are comparing two integers or booleans.
			case1 = buildITE(right, case2, case3, left)
			
			code.append(buildITE(tmpColor0, case0, case1, TAG_MASK, 'je', True))
		
		elif isinstance(node, ast.Ne):
			tagType = None
				
			case0 = Block()
			
			#Build the case where we need to call the not_equal function.
			case0.append(OneOp('push', right))
			case0.append(OneOp('push', left))
			case0.append(OneOp('call', ast.Name('not_equal'), None))
			case0.append(TwoOp('sub', Immediate(8), esp))
			case0.append(tag(eax, BOOL))
			
			if eax != dest:
				case0.append(move(eax, tmpColor0))
			
			case2 = move(FALS, tmpColor0)
			case3 = move(TRU, tmpColor0)
			
			#Build the case where we are comparing two integers or booleans.
			case1 = buildITE(right, case2, case3, left)
			
			code.append(buildITE(tmpColor0, case0, case1, TAG_MASK, 'jz', True))
		
		elif isinstance(node, ast.Is):
			case0 = move(FALS, tmpColor0)
			case1 = move(TRU, tmpColor0)
			
			code.append(buildITE(right, case0, case1, left))
		
		###########
		# Cleanup #
		###########
		
		#Re-tag left, right, and result appropriately.
		code.append(tag(tmpColor0))
		
		if origLeft != dest and left != dest and isinstance(origLeft, Register) and origLeft in toColors(node['post-alive']):
			code.append(tag(origLeft))
		
		if origRight != dest and right != dest and isinstance(origRight, Register) and origRight in toColors(node['post-alive']):
			code.append(tag(origRight))
		
		#Move the result.
		if tmpColor0 != dest:
			code.append(move(tmpColor0, dest))
		
		###############
		# End Cleanup #
		###############
		
		return code
	
	elif isinstance(node, ast.Boolean):
		if isinstance(node, ast.Tru):
			return TRU
		
		elif isinstance(node, ast.Fals):
			return FALS
	
	elif isinstance(node, ast.FunctionCall):
		code = Block()
		
		usedColors = toColors(node['pre-alive'])
		
		#Save any caller saved registers currently in use.
		saveRegs(code, caller, usedColors)
		
		addSize = 0
		args = list(node.args)
		args.reverse()
		for arg in args:
			src = selectInstructions(arg, cf)
			
			#Pack immediates if they haven't been packed yet.
			if isinstance(src, Immediate):
				src = pack(src, INT)
			
			code.append(OneOp('push', src))
			addSize += 4
		
		#Make the function call.
		code.append(OneOp('call', node.name, None))
		
		#Restore the stack.
		if addSize > 0:
			code.append(TwoOp('add', Immediate(addSize), esp))
		
		#Tag the result if necessary.
		code.append(tag(eax, node.tag))
		
		#Move the result into the proper destination.
		if dest and dest != eax:
			code.append(move(eax, dest))
		
		#Restore any caller saved registers that are in use.
		restoreRegs(code, caller, usedColors)

		return code
	
	elif isinstance(node, ast.If):
		cond = selectInstructions(node.cond, cf)
		then = selectInstructions(node.then, cf)
		els  = selectInstructions(node.els, cf)
		
		return buildITE(cond, then, els)
	
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
		code.append(move(esp, ebp))
		
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
		endBlock.append(move(Immediate(0), eax))
		#Restore the %esp and %ebp registers.
		endBlock.append(Instruction('leave'))
		#Return
		endBlock.append(Instruction('ret'))

		code.append(endBlock)
		
		return code
	
	elif isinstance(node, ast.Symbol):
		if node.has_key('color'):
			return node['color']
		else:
			raise Exception("Uncolored symbol ({0}) encountered.".format(node))
	
	elif isinstance(node, ast.UnaryOp):
		code = Block()
		
		src = selectInstructions(node.operand, cf)
		
		#########
		# Setup #
		#########
		
		tmpColor = getTmpColor(cf, node) if isinstance(dest, Mem) else dest
		
		if src != tmpColor:
			code.append(move(src, tmpColor))
			tmpColor.tagged = src.tagged
		
		if tmpColor.tagged:
			code.append(untag(tmpColor))
		
		#############
		# End Setup #
		#############
		
		if isinstance(node, ast.Negate):
			code.append(OneOp('neg', tmpColor))
			
			tmpColor.tagged = False
			tmpColor.tag = INT
		
		elif isinstance(node, ast.Not):
			case0 = move(FALS, tmpColor)
			case1 = move(TRU, tmpColor)
			
			tmpColor.tagged = True
			
			code.append(buildITE(src, case0, case1, FALS, 'jle'))
		
		###########
		# Cleanup #
		###########
		
		if not tmpColor.tagged:
			code.append(tag(tmpColor, tmpColor.tag))
		
		if tmpColor != dest:
			code.append(move(tmpColor, dest))
		
		###############
		# End Cleanup #
		###############
		
		return code
