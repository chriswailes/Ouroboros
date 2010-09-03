#Author		= Chris Wailes <chris.wailes@gmail.com
#Project		= CSCI 5525 HW1
#Date		= 2010/08/24
#Description	= This file compiles the generated Python assembly code.

CC		= gcc
CFLAGS	= -O3 -Wall -fPIC -march=native
LFLAGS	= -lm -Lruntime/ -lpyrun

all: runtime

s: runtime
	for s in *.s; do \
		$(CC) $(CFLAGS) -o $${s%\.*} $$s $(LFLAGS); \
	done;

.PHONY: runtime
runtime: runtime-static

.PHONY: runtime-shared
runtime-shared:
	cd runtime; make shared-32
	cd runtime; make shared-64

.PHONY: runtime-static
runtime-static:
	cd runtime; make static-32
	cd runtime; make static-64

.PHONY: clean
clean:
	rm -f *.s
	rm -f *.pyc
	cd runtime; make clean
