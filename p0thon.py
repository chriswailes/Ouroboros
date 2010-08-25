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

ast = compiler.parse(inFile.read())

#Print their AST
print(ast)

#Generate my AST
ast = myAST.toMyAST(ast)

#Print my AST
print(ast)

print("\n")

#Flatten my AST
ast = ast.flatten()

#Print out the Python code for my flattened AST
print(ast.toPython())

assembly = ast.compile()

#Compile and print the AST
print(assembly)

#Put the compiled AST into the output file.
outFile.write(assembly)
