#!/usr/bin/python

"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW2
Date:		2010/09/08
Description:	A simple parser for p0.
"""

from frontend.lexer import tokens

from lib.ast import *

start = 'module'

precedence = (
		('nonassoc','PRINT'),
		('left','PLUS', 'RPAREN'),
		('right', 'NEG')
	)

######################
# Parser Definitions #
######################

def p_module1(t):
	'module : statement_list'
	t[0] = Module(t[1])

##############
# Statements #
##############

def p_statement0(t):
	'statement : PRINT arg_list0 NEWLINE'
	t[0] = FunctionCall(Name('print_int_nl'), t[2])

def p_statement1(t):
	'statement : PRINT LPAREN arg_list0 RPAREN NEWLINE'
	t[0] = FunctionCall(Name('print_int_nl'), t[3])

def p_statement2(t):
	'statement : NAME ASSIGN expression NEWLINE'
	t[0] = Assign(Name(t[1]), t[3])

def p_statement3(t):
	'statement : expression NEWLINE'
	t[0] = t[1]

###############
# Expressions #
###############

def p_expression0(t):
	'expression : NAME'
	t[0] = Name(t[1])

def p_expression1(t):
	'expression : INT'
	t[0] = Integer(t[1])

def p_expression2(t):
	'expression : NEG expression'
	t[0] = Negate(t[2])

def p_expression3(t):
	'expression : expression PLUS expression'
	t[0] = Add(t[1], t[3])

def p_expression4(t):
	'expression : LPAREN expression RPAREN'
	t[0] = t[2]

def p_expression5(t):
	'expression : INPUT LPAREN RPAREN'
	t[0] = FunctionCall(Name('input'), [])

########
# Util #
########

def p_stmt_list0(t):
	'statement_list : empty'
	
	t[0] = []

def p_stmt_list1(t):
	'statement_list : statement statement_list'
	
	stmts = [t[1]]
	stmts.extend(t[2])
	
	t[0] = stmts

def p_arg_list00(t):
	'arg_list0 : empty'
	t[0] = []

def p_arg_list01(t):
	'arg_list0 : expression arg_list1'
	
	exps = [t[1]]
	exps.extend(t[2])
	
	t[0] = exps

def p_arg_list10(t):
	'arg_list1 : empty'
	t[0] = []

def p_arg_list11(t):
	'arg_list1 : COMMA expression arg_list1'
	
	exps = [t[1]]
	exps.extend(t[2])
	
	t[0] = exps

def p_empty(t):
	'empty :'
	pass

def p_error(t):
	print "Syntax error at '{0}', line number {1}".format(t.value, t.lineno)

import ply.yacc as yacc
parser = yacc.yacc()
