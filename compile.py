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
from assembler.coloring import ColorFactory
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
		print('')
	
	##################
	# AST Generation #
	##################
	tree = translate(tree)
	
	if config.verbose:
		#Print my AST
		print(tree)
		print('')
	
	cf = ColorFactory()
	
	#######################
	# AST Transformations #
	#######################
	
	#Constant folding and propigation and discarding of useless nodes.
	runTransform(tree, ['const_prop', 'discard', 'const_fold'])
	
	#Simplification, declassification, and flattening of the AST.
	runTransform(tree, ['simplify', 'flatten'])
	
	#Function migration.
	runTransform(tree, 'function_migration')
	
	#Another round of constant propigation to take care of new constants
	#introduced by the other passes.
	runTransform(tree, ['const_prop', 'discard', 'const_fold'])
	
	#Symbol coloring.
	runTransform(tree, 'color', {'cf':cf})
	
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
	
	#########################
	# Instruction Selection #
	#########################
	
	while True:
		#Attempt to compile the AST.  If a spill occurs we catch it and run
		#the spill transformation before trying to color the AST again.  This
		#process will continue until a successful coloring is found.
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
