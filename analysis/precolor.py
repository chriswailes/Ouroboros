"""
Author:		Chris Wailes <chris.wailes@gmail.com>
Project:		Ouroboros
Date:		2010/12/08
Description:	This analysis pass is a wrapper around the architecture specific
			precoloring analysis passes.
"""

args		= []
prereqs	= []
result	= ''
sets		= ['precolor']

from lib.config import config

def init():
	from analysis.pass_manager import register
	register('precolor', precolor, args, prereqs, result, sets)

def precolor(tree):
	if config.arch == 'x86':
		from x86 import precolor as arch
	
	elif config.arch == 'x86_64':
		from x86_64 import precolor as arch
	
	arch.precolor(tree)
