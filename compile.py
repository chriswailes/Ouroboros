#!/usr/bin/python -O

"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/08/26
Description:	This file is the actual compiler.
"""

import compiler

import os

from analysis.pass_manager import runPass

from assembler import *
from assembler.redundant_moves import redundantMoves
from assembler.instruction_selection import selectInstructions

from lib import ast, util
from lib.translate import translate
from lib.config import config, args

from transforms.pass_manager import runTransform

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
	
	#Run the AST transformation passes.
	runTransform(tree, ['const_prop', 'discard', 'const_fold'])
	runTransform(tree, 'flatten')
	runTransform(tree, 'function_migration')
	#~runTransforms(tree, ['const_prop'])
	#~cf = runTransform(tree, 'color', {'cf':None})
	
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
	
	exit(0)
	
	#One of the symbols from each of these sets needs to be spilled.
	spillSets = []
	
	#Try and compile the AST, catching spills and iterating until they are all
	#resolved.
	while True:
		try:
			#Compile the AST.
			assembly = selectInstructions(tree, cf)
			break
		
		except Spill as s:
			if config.verbose:
				print("Caught a spill.")
			
			spillSets.append(s.symbols)
			
			cf = runTransform(tree, 'spill', {'spillSets':spillSets})
			runTransform(tree, 'color', {'cf':cf})

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
