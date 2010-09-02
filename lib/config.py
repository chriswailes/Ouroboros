"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/09/02
Description:	Code for generating the configuration for the compiler.
"""

from optparse import OptionParser
from os import path

runtimePath = path.abspath(path.join(path.dirname(path.abspath(__file__)), '..', 'runtime'))

parser = OptionParser()

parser.add_option('-a', '--arch', dest = 'arch', default = 'x86',
	help = 'The architecture to compile for.')

parser.add_option('-l', '--lib', dest = 'lib', default = runtimePath,
	help = 'The path to the pycom runtime libraries.')

parser.add_option('-s', action = 'store_const', const = 'compile',
	dest = 'target_stage', default = 'full',
	help = 'Stop after compilation into assembly code.  Do not assemble.')

parser.add_option('-v', '--verbose', action = 'store_true',
	dest = 'verbose', default = False, help = 'Print additional output.')

config, args = parser.parse_args()
