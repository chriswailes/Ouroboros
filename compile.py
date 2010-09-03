#!/usr/bin/python

"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/08/26
Description:	This file is the actual compiler.
"""

import compiler

import os
import os.path

from assembler.redundant_moves import redundantMoves
from assembler.instruction_selection import selectInstructions

from lib import ast, util

from lib.config import config, args

from transforms.const_fold import foldConstants
from transforms.discard import discard
from transforms.flatten import flatten

if len(args) == 0:
	print('No input files specified.')
	exit(0)

inFile = open(config.inName)

tokens = inFile.read()

#Generate my AST
tree = ast.toMyAST(compiler.parse(tokens))

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

if config.target_stage == 'full':
	command = "gcc {0} -o {1} {2} {3} ".format(config.cflags, config.outName, config.sName, config.lflags)
	
	if config.verbose:
		print(command)
	
	os.system(command)
	os.remove(config.sName)
