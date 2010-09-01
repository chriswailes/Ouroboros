#Author		= Chris Wailes <chris.wailes@gmail.com
#Project		= CSCI 5525 HW1
#Date		= 2010/08/24
#Description	= This file compiles the generated Python assembly code.

CC		= gcc
CONDFLAGS	= -march=native -m32
CFLAGS	= -O3 -Wall -fPIC $(CONDFLAGS)
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
	cd runtime; make shared CONDFLAGS="$(CONDFLAGS)"

.PHONY: runtime-static
runtime-static:
	cd runtime; make static CONDFLAGS="$(CONDFLAGS)"

.PHONY: clean
clean:
	rm -f *.s
	rm -f *.pyc
	cd runtime; make clean
