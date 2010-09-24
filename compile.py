#!/usr/bin/python -O

"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/08/26
Description:	This file is the actual compiler.
"""

import compiler

import os

from assembler import *
from assembler.redundant_moves import redundantMoves
from assembler.instruction_selection import selectInstructions

from lib import ast, util
from lib.translate import translate
from lib.config import config, args

from transforms.pass_manager import runTransform

#~from transforms.coloring import color, clearColoring, spill
#~from transforms.const_fold import foldConstants
#~from transforms.const_prop import propigateConstants
#~from transforms.discard import discard
#~from transforms.fixedpoint import fixedpoint
#~from transforms.flatten import flatten

if len(args) == 0:
	print('No input files specified.')
	exit(0)

if config.startStage == 'python':
	inFile = open(config.inName)

	tokens = inFile.read()
	tree = compiler.parse(tokens)
	
	if config.verbose:
		#Print the original AST
		print(tree)
		print("")
	
	#Generate my AST	
	tree = translate(tree)
	
	if config.verbose:
		#Print my AST
		print(tree)
		print("")
	
	#Run the AST transformation passes (except 'color', which is done in the
	#loop below.
	runTransform(tree, ['const_prop', 'discard', 'const_fold'])
	runTransform(tree, 'flatten')
	
	if config.verbose:
		#Print my flattened (and folded) AST
		print(tree)
		print('')
		
		#Print out the original program.
		print("Before Transformation Passes:")
		print(tokens)
		
		#Print out the Python code for my flattened AST
		print("After Transformation Passes:")
		print(tree.toPython())
		print('')
	
	#One of the symbols from each of these sets needs to be spilled.
	spillSets = []
	
	#Try and compile the AST, catching spills and iterating until they are all
	#resolved.
	while True:
		try:
			#Compile the AST.
			cf = runTransform(tree, 'color')
			assembly = selectInstructions(tree, cf)
			break
		
		except Spill as s:
			spillSets.append(s.symbols)
			
			runTransform(tree, 'spill', {'spillSets':spillSets})

	"""
	if config.verbose:
		#Print out the pre-assembly passes code.
		print("Before Assembly Passes")
		print(assembly)

	#Run the instruction passes.
	redundantMoves(assembly)

	if config.verbose:
		#Print out the post-assembly passes code.
		print("After Assembly Passes")
		print(assembly)
	"""

	#Put the produced assembly into the output file.
	outFile = open(config.sName, 'w')
	outFile.write(str(assembly))
	outFile.close()

if config.targetStage == 'full':
	if config.verbose:
		print(config.compileCommand)
	
	os.system(config.compileCommand)
	
	if config.startStage != 'assembly':
		os.remove(config.sName)
