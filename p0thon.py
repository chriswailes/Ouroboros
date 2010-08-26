#!/usr/bin/python

import compiler
import os.path
import sys

import myAST

if len(sys.argv) < 2:
	print("Insufficient number of arguments.")
	exit(0)

inFile = open(sys.argv[1])

outName = os.path.basename(sys.argv[1])[0:-3] + ".s"
outFile = open(outName, "w")

program = inFile.read()

ast = compiler.parse(program)

#Generate my AST
ast = myAST.toMyAST(ast)

#Print my AST
print(ast)

#Flatten my AST.
ast.flatten()

#Print my flattened AST
print(ast)

print("\n")

#Print out the original program.
print("Original:")
print(program)

#Print out the Python code for my flattened AST
print("Flat:")
print(ast.toPython())

#Compile the AST.
assembly = ast.compile()

#Print the AST
print(assembly)

#Put the compiled AST into the output file.
outFile.write(assembly)
