#!/usr/bin/python

"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/08/26
Description:	This file is the actual compiler.
"""

import compiler
import os.path
import sys

from assembler.redundant_moves import redundantMoves
from lib import ast, util
from transforms.flatten import flatten

if len(sys.argv) < 2:
	print("Insufficient number of arguments.")
	exit(0)

inFile = open(sys.argv[1])

outName = os.path.basename(sys.argv[1])[0:-3] + ".s"
outFile = open(outName, "w")

tokens = inFile.read()

tree = compiler.parse(tokens)

#Generate my AST
tree = ast.toMyAST(tree)

#Print my AST
print(tree)
print("")

#Flatten my AST.
tree = flatten(tree)

#Print my flattened AST
print(tree)

print("\n")

#Print out the original program.
print("Original:")
print(tokens)

#Print out the Python code for my flattened AST
print("Flat:")
print(tree.toPython())

#Compile the AST.
assembly = tree.compile()

#Print out the pre-assembly passes code.
print("Before Assembly Passes")
print(assembly)

#Run the instruction passes.
redundantMoves(assembly)

#Print the AST
print("After Assembly Passes")
print(assembly)

#Put the compiled AST into the output file.
outFile.write(str(assembly))
