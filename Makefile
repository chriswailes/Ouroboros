#Author		= Chris Wailes <chris.wailes@gmail.com
#Project		= CSCI 5525 HW1
#Date		= 2010/08/24
#Description	= This file compiles the generated Python assembly code.

CC		= gcc
CFLAGS	= -O3 -arch=native -march=native -Wall -m32

all: input

input: input.S runtime.o
	$(CC) $(CFLAGS) -o $@ input.S runtime.o hashtable_itr.o hashtable.o

hashtable.o: hashtable.c hashtable.h hashtable_itr.o
	$(CC) $(CFLAGS) -c $<

hashtable_itr.o: hashtable_itr.c hashtable_itr.h
	$(CC) $(CFLAGS) -c $<

runtime.o: runtime.c runtime.h hashtable.o
	$(CC) $(CFLAGS) -c $<

.PHONY: clean
clean:
	rm -f *.o
