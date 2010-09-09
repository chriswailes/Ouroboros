#!/usr/bin/python

"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW2
Date:		2010/09/08
Description:	A simple lexer for p0.
"""

reserved = {
		'print' : 'PRINT',
		'input' : 'INPUT'
	}

tokens = ['INT', 'PLUS', 'NEG', 'NAME', 'ASSIGN', 'LPAREN', 'RPAREN', 'COMMA', 'NEWLINE'] + list(reserved.values())

#####################
# Lexer Definitions #
#####################

t_ASSIGN			= r'='

t_COMMA			= r','

t_LPAREN			= r'\('

t_RPAREN			= r'\)'

t_PLUS			= r'\+'

t_NEG			= r'-'

t_ignore_COMMENT	= r'\#.*'

t_ignore			= ' \t'

def t_NAME(t):
	r'[a-zA-Z_][a-zA-Z0-9_]*'
	
	t.type = reserved.get(t.value, 'NAME')    # Check for reserved words
	return t

def t_INT(t):
	r'-?\d+'
	
	try:
		t.value = int(t.value)
	except ValueError:
		print "integer value too large", t.value
		t.value = 0
	
	return t

def t_NEWLINE(t):
	r'\n+'
	t.lexer.lineno += t.value.count("\n")
	
	return t

def t_error(t):
	print "Illegal character '%s'" % t.value[0]
	t.lexer.skip(1)
  
  
import ply.lex as lex
lexer = lex.lex()

#############
# Main Code #
#############

if __name__ == '__main__':
	import sys
	
	inFile = open(sys.argv[1])
	
	lexer.input(inFile.read())

	tokens = []
	token = lexer.token()

	while token:
		tokens.append(token)
		token = lexer.token()

	print(tokens)
