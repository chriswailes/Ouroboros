#!/usr/bin/python -O

"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/08/26
Description:	This file is the actual compiler.
"""

import compiler

import os

from analysis.liveness import *
from analysis.stats import *

from assembler.redundant_moves import redundantMoves
from assembler.instruction_selection import selectInstructions

from lib import ast, util
from lib.translate import translate
from lib.config import config, args

from transforms.fixedpoint import fixedpoint
from transforms.const_fold import foldConstants
from transforms.const_prop import propigateConstants
from transforms.discard import discard
from transforms.flatten import flatten

if len(args) == 0:
	print('No input files specified.')
	exit(0)

if config.startStage == 'python':
	inFile = open(config.inName)

	tokens = inFile.read()
	tree = compiler.parse(tokens)
	
	if config.verbose:
		print(tree)
		print("")
	
	#Generate my AST	
	tree = translate(tree)
	
	if config.verbose:
		#Print my AST
		print(tree)
		print("")
	
	#Run the AST transformation passes
	#tree = fixedpoint(tree, discard, propigateConstants, foldConstants)
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
	
	countReads(tree)
	livenessAST(tree)
	calculateSpans(tree)
	
	#~for line in tree.block:
		#~print line.toPython()
		#~print("pre-alive: " + str(line['pre-alive']))
		#~print("post-alive: " + str(line['post-alive']))
		#~print('')
	
	for sym in tree.collectSymbols():
		print("{0}: {1}".format(str(sym), str(sym['span'])))
	
	exit(0)
	
	calculateSpans(tree)
	
	for sym in tree.collectSymbols():
		print("{0} -> {1:d}".format(str(sym), sym['reads']))
	
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
