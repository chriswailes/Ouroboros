#Author		= Chris Wailes <chris.wailes@gmail.com
#Project		= Ouroboros
#Date		= 2010/09/03
#Description	= Makefile for pycom/assembler

SUBDIRS	= x86 x86_64

.PHONY: clean
clean:
	rm -f *.pyc *.pyo
	
	for sd in $(SUBDIRS); do (cd $$sd; make clean); done
