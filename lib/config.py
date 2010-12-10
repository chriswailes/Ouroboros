"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		Ouroboros
Date:		2010/09/02
Description:	Code for generating the configuration for the compiler.
"""

from optparse import OptionParser
from os import path
import re

runtimePath = path.abspath(path.join(path.dirname(path.abspath(__file__)), '..', 'runtime'))

################
# User Options #
################

parser = OptionParser()

parser.add_option('-a', '--arch', dest = 'arch', default = 'x86',
	help = 'The architecture to compile for.')

parser.add_option('-l', '--lib', dest = 'lib', default = runtimePath,
	help = 'The path to the pycom runtime libraries.')

parser.add_option('-o', '--output', dest = 'outName', default = None,
	help = 'The file to produce as output.  The default is determined by\
	name of the input file.')

parser.add_option('-s', action = 'store_const', const = 'compile',
	dest = 'targetStage', default = 'full',
	help = 'Stop after compilation into assembly code.  Do not assemble.')

parser.add_option('-v', '--verbose', action = 'store_true',
	dest = 'verbose', default = False, help = 'Print additional output.')

config, args = parser.parse_args()

##############
# File Names #
##############

inName = args[0]
setattr(config, 'inName', inName)

mo = re.search("(.+)\.([a-zA-Z0-9]+)$", path.basename(inName))

if mo.group(1):
	outName = config.outName or mo.group(1)
	setattr(config, 'outName', outName)
else:
	raise Exception("Input file name invalid.")

sName = config.outName + '.s'
setattr(config, 'sName', sName)

if mo.group(2) == 'py':
	setattr(config, 'startStage', 'python')
elif mo.group(2) == 's':
	setattr(config, 'startStage', 'assembly')
else:
	raise Exception("Unknown input file type.")

###############
# GCC Strings #
###############

cflags = '-O3 -Wall -fPIC -march=native'
lflags = "-lm -L\"{0}\"".format(config.lib)

if config.arch == 'x86':
	cflags += " -m32"
	lflags += " -lpyrun32"
elif config.arch == 'x86_64':
	cflags += " -m64"
	lflags += " -lpyrun64"
else:
	raise Exception("Unsupported architecture specified.")

setattr(config, 'cflags', cflags)
setattr(config, 'lflags', lflags)

command = "gcc {0} -o \"{1}\" \"{2}\" {3} ".format(config.cflags, config.outName, config.sName, config.lflags)
setattr(config, 'compileCommand', command)
