#!/usr/bin/python

import compiler
import sys

import myAST

if len(sys.argv) < 3:
	print("Insufficient number of arguments.")
	exit(0)

inFile = open(sys.argv[1])
outFile = open(sys.argv[2], "w")

ast = compiler.parse(inFile.read())

#Print their AST
print(ast)

#Generate my AST
ast = myAST.toMyAST(ast)

#Print my AST
print(ast)

print("\n\n")

#Flatten my AST
ast = ast.flatten()

#Print out the Python code for my flattened AST
print(ast.toPython())

assembly = ast.compile()

#Compile and print the AST
print(assembly)

#Put the compiled AST into the output file.
outFile.write(assembly)
