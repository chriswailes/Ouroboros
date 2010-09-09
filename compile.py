#!/usr/bin/python -O

"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/08/26
Description:	This file is the actual compiler.
"""

import compiler

import os

from frontend.parser import parser

from assembler.redundant_moves import redundantMoves
from assembler.instruction_selection import selectInstructions

from lib import ast, util
from lib.translate import translate
from lib.config import config, args

from transforms.const_fold import foldConstants
from transforms.discard import discard
from transforms.flatten import flatten

if len(args) == 0:
	print('No input files specified.')
	exit(0)

if config.startStage == 'python':
	inFile = open(config.inName)

	tokens = inFile.read()

	#Generate my AST
	tree = translate(compiler.parse(tokens))
	#tree = parser.parse(tokens)

	if config.verbose:
		#Print my AST
		print(tree)
		print("")

	#Run the AST transformation passes
	tree = discard(tree)
	tree = foldConstants(tree)
	tree = flatten(tree)

	if config.verbose:
		#Print my flattened (and folded) AST
		print(tree)
		
		print("\n")
		
		#Print out the original program.
		print("Original:")
		print(tokens)
		
		#Print out the Python code for my flattened AST
		print("Flat:")
		print(tree.toPython())
		print("\n")
	
	#Compile the AST.
	assembly = selectInstructions(tree)

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
