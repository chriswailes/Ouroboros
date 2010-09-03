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

parser.add_option('-o', '--output', dest = 'outName', default = None,
	help = 'The file to produce as output.  The default is determined by\
	name of the input file.')

parser.add_option('-s', action = 'store_const', const = 'compile',
	dest = 'target_stage', default = 'full',
	help = 'Stop after compilation into assembly code.  Do not assemble.')

parser.add_option('-v', '--verbose', action = 'store_true',
	dest = 'verbose', default = False, help = 'Print additional output.')

config, args = parser.parse_args()

inName = args[0]
setattr(config, 'inName', inName)

outName = config.outName or path.basename(args[0])[0:-3]
setattr(config, 'outName', outName)

sName = outName + '.s'
setattr(config, 'sName', sName)

cflags = "-O3 -Wall -fPIC -march=native -m32"
lflags = "-lm -L\"{0}\" -lpyrun32".format(config.lib)

setattr(config, 'cflags', cflags)
setattr(config, 'lflags', lflags)
