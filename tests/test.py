#!/usr/bin/python

"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		CSCI 5525 HW1
Date:		2010/09/03
Description:	A program for testing the pycom compiler.
"""

from glob import glob

from optparse import OptionParser

import os
import os.path as path

import re
from subprocess import Popen, PIPE, STDOUT

import shutil
import sys

bnre = re.compile("(.+)\.[a-zA-Z0-9]+$")

basedir = './'
outdir = path.join(basedir, 'output')

dirs = ['p0', 'p0.5', 'p1', 'p2', 'hw1', 'hw4', 'hw5', 'hw6', 'benchmarks']

OKGREEN	= '\033[92m'
FAILRED	= '\033[91m'
ENDC		= '\033[0m'

parser = OptionParser()

parser.add_option('-a', '--arch', dest = 'arch', default = 'x86',
	help = 'The architecture to compile for.')

config, args = parser.parse_args()

#Clean the output directory.
for f in glob(path.join('output', '*')):
	shutil.rmtree(f)

for d in dirs:
	print("New test set: {0}".format(d))
	
	os.mkdir(path.join(outdir, d))
	
	maxLen = 0
	for f in glob(path.join(d, '*.py')):
		if len(f) > maxLen:
			maxLen = len(f)
	
	fmtS = "\t{0:" + str(maxLen + 5) + "} "
	
	for f in sorted(glob(path.join(d, '*.py'))):
		mo = bnre.match(f)
		
		inF = mo.group(1) + '.in'
		outF = path.join(outdir, d, path.basename(mo.group(1)))
		
		if path.exists(inF):
			sys.stdout.write(fmtS.format(f))
			sys.stdout.flush()
			
			#Compile the file.
			command = "ouroboros -o {0} -a {1} {2}".format(outF, config.arch, f)
			sp = Popen(command, shell = True, stdout = PIPE, stderr = STDOUT)
			sp.wait()
			
			#Run the file.
			command = "{0} < {1} 2>&1".format(outF, inF)
			sp = Popen(command, shell = True, stdout = PIPE)
			sp.wait()
			cOut = sp.communicate()[0]
			
			#Interpret the progrm through Python.
			command = "python {0} < {1}".format(f, inF)
			sp = Popen(command, shell = True, stdout = PIPE)
			sp.wait()
			iOut = sp.communicate()[0]
			
			if iOut == cOut:
				print(OKGREEN + "OK" + ENDC)
			else:
				print(FAILRED + "FAIL" + ENDC)
	
	print("")

