#!/usr/bin/python

import compiler
import sys

import myAST

f = open(sys.argv[1])

ast = compiler.parse(f.read())

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
