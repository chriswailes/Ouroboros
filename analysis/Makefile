# Author		= Chris Wailes <chris.wailes@gmail.com
# Project		= Ouroboros
# Date		= 2010/09/19
# Description 	= Makefile for pycom/analysis

SUBDIRS	= x86

.PHONY: clean
clean:
	rm -f *.pyc *.pyo
	
	for sd in $(SUBDIRS); do (cd $$sd; make clean); done
